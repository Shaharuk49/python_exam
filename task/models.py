from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UrlData(models.Model):
    url = models.URLField(max_length=200)
    slug = models.CharField(max_length=10, unique=True)
    time= models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.url