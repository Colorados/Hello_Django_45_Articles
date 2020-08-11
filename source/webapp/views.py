from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Article, STATUS_CHOICES
# from django.urls import reverse
from django.http import HttpResponseNotAllowed
from webapp.forms import ArticleForm


def index_view(request):
    is_admin = request.GET.get('is_admin', None)
    if is_admin:
        data = Article.objects.all()
    else:
        data = Article.objects.filter(status='moderated')
    return render(request, 'index.html', context={
        'articles': data
    })


def article_view(request, pk):
    # article = Article.objects.filter(pk=article_id)
    # if len(article) == 0:
    #     raise Http404

    # try:
    #     article = Article.objects.get(pk=article_id)
    # except Article.DoesNotExist:
    #     raise Http404
    article = get_object_or_404(Article, pk=pk)
    context = {'article': article}
    return render(request, 'article_view.html', context)


def article_create_view(request):
    if request.method == "GET":
        form = ArticleForm()
        return render(request, "article_create.html", context={'form': form})
    elif request.method == "POST":
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            # article = Article.objects.create(**form.cleaned_data)
            article = Article.objects.create(title=form.cleaned_data['title'],
                                             text=form.cleaned_data['text'],
                                             author=form.cleaned_data['author'],
                                             status=form.cleaned_data['status'])
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, "article_create.html", context={'form': form})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
    

def article_update_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        form = ArticleForm(initial={'title': article.title,
                                    'text': article.text,
                                    'author': article.author,
                                    'status': article.status})
        return render(request, "article_update.html", context={'form': form,
                                                               'article': article})
    elif request.method == "POST":
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.text = form.cleaned_data['text']
            article.author = form.cleaned_data['author']
            article.status = form.cleaned_data['status']
            article.save()
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, "article_update.html", context={'article': article,
                                                                   'form': form})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])