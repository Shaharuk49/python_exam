from django.contrib import admin
from .models import UrlData

@admin.register(UrlData)
class UrlDataAdmin(admin.ModelAdmin):
    list_display = ('url', 'slug', 'time')
    search_fields = ('url', 'slug')
    ordering = ('-time',)