from django.contrib import admin
from webapp.models import Article, ArticleAdmin

admin.site.register(Article, ArticleAdmin)
