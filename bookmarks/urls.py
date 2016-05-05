from django.conf.urls import url

from .views import BookmarksListView

urlpatterns = [
    url(r'$', BookmarksListView.as_view(), name='bookmark-list')
]