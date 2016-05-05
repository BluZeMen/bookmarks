from django.forms import ModelForm
from .models import Bookmark


class BookmarkCreateForm(ModelForm):
    class Meta:
        model = Bookmark
        fields = ['url']
