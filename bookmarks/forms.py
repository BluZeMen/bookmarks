"""Forms module

This module describes forms
"""
from django.forms import ModelForm

from .models import Bookmark


class BookmarkCreateForm(ModelForm):
    class Meta:
        model = Bookmark
        fields = ['url']
