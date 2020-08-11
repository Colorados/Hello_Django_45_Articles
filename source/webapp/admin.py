from django.contrib import admin
from webapp.models import Article, ArticleAdmin, Comment

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
