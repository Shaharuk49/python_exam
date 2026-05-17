from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UrlData(models.Model):
    url = models.URLField(max_length=200)
    slug = models.CharField(max_length=10, unique=True)
    time = models.DateTimeField(default=timezone.now)
    total_clicks = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return self.url
    

class ClickAnalytics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    short_url = models.ForeignKey(UrlData, on_delete=models.CASCADE, related_name='clicks')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True) 
    refer = models.URLField(null=True, blank=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Click on {self.short_url.slug} at {self.timestamp}"
