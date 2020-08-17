from django.contrib import admin
from webapp.models import Article, ArticleAdmin, Comment, ArticleTag, Tag


class ArticleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(ArticleTag)
admin.site.register(Tag)
