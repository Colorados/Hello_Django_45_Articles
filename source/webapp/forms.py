from django import forms
from django.core.exceptions import ValidationError

from .models import STATUS_CHOICES
from .models import Article, Tag

default_status = STATUS_CHOICES[0][0]


BROWSER_DATETIME_FORMAT = '%Y-%m-%dT%H:%M'


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label='Заголовок')
    text = forms.CharField(max_length=3000, required=True, label='Текст', widget=forms.Textarea)
    author = forms.CharField(max_length=40, required=True, label='Автор', initial='Unknown')
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True, label='Статус', initial=default_status)
    published = forms.DateTimeField(required=False, label='Время публикации',
                                    input_formats=['%Y-%m-%d', BROWSER_DATETIME_FORMAT, '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'],
                                    widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),required=False, label='Теги', widget=forms.SelectMultiple)

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if len(title) < 10:
    #         raise ValidationError('Title is too short!')
    #     return title

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if len(title) < 10:
    #         raise ValidationError('This field should be at least %(length)d symbols long!', code='too_short',
    #                               params={'length': 10})
    #     return title

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
        author = cleaned_data.get('author')
        if text and title and text == title:
            errors.append(ValidationError("Text of the article should not duplicate it's title!"))
        if title and author and title == author:
            errors.append(ValidationError("Author of the article should not duplicate it's title!"))
        if errors:
            raise ValidationError(errors)
        return cleaned_data


class CommentForm(forms.Form):
    article = forms.ModelChoiceField(queryset=Article.objects.all(), required=True, label='Статья')