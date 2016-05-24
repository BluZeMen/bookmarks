"""Admin module

This module used for registrating models in the Django admin.

"""

from django.contrib import admin
from django.contrib.admin import register

from bookmarks.models import Bookmark


@register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """
    Bookmark admin entity
    """
    list_display = ('title', 'description', 'url')
    search_fields = ('title', 'description')


