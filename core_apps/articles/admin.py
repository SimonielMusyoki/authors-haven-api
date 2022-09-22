from django.contrib import admin

from . import models


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "author", "slug", "article_read_time", "views"]
    list_display_links = ["pkid", "id"]
