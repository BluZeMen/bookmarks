from urllib.error import HTTPError
from urllib.parse import urlparse

from django.db import models
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

# Create your models here.


class Bookmark(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    favicon = models.URLField(max_length=64, blank=True, null=True)
    url = models.URLField(max_length=128, unique=True)

    def is_parsed(self):
        return self.title is not None or self.description is not None or self.favicon is not None