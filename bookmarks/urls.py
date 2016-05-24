"""Urls module

This used for dispatching requests to django
"""
from django.conf.urls import url

from .views import BookmarksListView

urlpatterns = [
    url(r'^$', BookmarksListView.as_view(), name='index')
]