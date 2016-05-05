from django.contrib import admin
from django.contrib.admin import register
from bookmarks.models import Bookmark

# Register your models here.


@register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'url')
    search_fields = ('title', 'description')


