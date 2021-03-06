from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.utils.timezone import make_naive
from django.views.generic import View, TemplateView, FormView
from .base_views import FormView as CustomFormView
from webapp.models import Article
from webapp.forms import ArticleForm
from .forms import BROWSER_DATETIME_FORMAT


class IndexView(View):
    def get(self, request):
        is_admin = request.GET.get('is_admin', None)
        if is_admin:
            data = Article.objects.all()
        else:
            data = Article.objects.filter(status='moderated')
        search = request.GET.get('search')
        if search:
            data = data.filter(title__icontains=search)
        return render(request, 'index.html', context={
            'articles': data
        })


class ArticleView(TemplateView):
    template_name = 'article_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        context['article'] = article
        return context


class ArticleCreateView(CustomFormView):
    template_name = 'article_create.html'
    form_class = ArticleForm

    def form_valid(self, form):
        data = {}
        tags = form.cleaned_data.pop('tags')
        for key, value in form.cleaned_data.items():
            if value is not None:
                data[key] = value
        self.article = Article.objects.create(**data)
        self.article.tags.set(tags)
        return super().form_valid(form)

    def get_redirect_url(self):
        return reverse('article_view', kwargs={'pk': self.article.pk})
    

class ArticleUpdateView(FormView):
    template_name = 'article_update.html'
    form_class = ArticleForm

    def dispatch(self, request, *args, **kwargs):
        self.article = self.get_object()
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.article
        return context

    def get_initial(self):
        initial = {}
        for key in 'title', 'text', 'author', 'status':
            initial[key] = getattr(self.article, key)
        initial['published'] = make_naive(self.article.published).strftime(BROWSER_DATETIME_FORMAT)
        return initial

    def form_valid(self, form):
        tags = form.cleaned_data.pop('tags')
        for key, value in form.cleaned_data.items():
            if value is not None:
                setattr(self.article, key, value)
        self.article.save()
        self.article.tags.set(tags)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.article.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'article_delete.html', context={'article': article})
    elif request.method == 'POST':
        article.delete()
        return redirect('home')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])