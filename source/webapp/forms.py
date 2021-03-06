from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible


from .models import STATUS_CHOICES
from .models import Article, Tag

default_status = STATUS_CHOICES[0][0]


BROWSER_DATETIME_FORMAT = '%Y-%m-%dT%H:%M'

#
# def at_least_10(string):
#     if len(string) < 10:
#         raise ValidationError('Title is too short!')
#

@deconstructible
class MinLengthValidator(BaseValidator):
    message = 'Value "%(value)s" has length of %(show_value)d! It should be at least %(limit_value)d symbols long!'
    code = 'too_short'

    def compare(self, value, limit):
        return value < limit

    def clean(self, value):
        return len(value)


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label='Заголовок', validators=[MinLengthValidator(10)])
    text = forms.CharField(max_length=3000, required=True, label='Текст', widget=forms.Textarea)
    author = forms.CharField(max_length=40, required=True, label='Автор', initial='Unknown')
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True, label='Статус', initial=default_status)
    published = forms.DateTimeField(required=False, label='Время публикации',
                                    input_formats=['%Y-%m-%d', BROWSER_DATETIME_FORMAT, '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'],
                                    widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),required=False, label='Теги', widget=forms.SelectMultiple)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     errors = []
    #     title = cleaned_data.get('title')
    #     text = cleaned_data.get('text')
    #     author = cleaned_data.get('author')
    #     if text and title and text == title:
    #         errors.append(ValidationError("Text of the article should not duplicate it's title!"))
    #     if title and author and title == author:
    #         errors.append(ValidationError("Author of the article should not duplicate it's title!"))
    #     if errors:
    #         raise ValidationError(errors)
    #     return cleaned_data


class CommentForm(forms.Form):
    article = forms.ModelChoiceField(queryset=Article.objects.all(), required=True, label='Статья')