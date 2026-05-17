from django.contrib import admin
from .models import UrlData
from .models import ClickAnalytics

admin.site.register(UrlData)
admin.site.register(ClickAnalytics)