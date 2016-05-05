from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect

from bookmarks.forms import BookmarkCreateForm
from .models import Bookmark
from .bookmark_parser import parse_bookmark



class BookmarksListView(FormView):
    template_name = 'bookmarks/list.html'
    success_url = '/'
    form_class = BookmarkCreateForm

    def get_context_data(self, **kwargs):
        context = super(BookmarksListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['bookmarks'] = Bookmark.objects.filter(user=self.request.user)
        else:
            context['bookmarks'] = []
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        parse_bookmark(form.instance)
        return HttpResponseRedirect(self.get_success_url())


