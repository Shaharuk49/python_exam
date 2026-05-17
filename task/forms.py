
from datetime import timezone

from django import forms
from .models import UrlData

class ShortenUrlForm(forms.Form):
    url = forms.URLField(label="Enter your URL here", widget=forms.URLInput(attrs={'placeholder': 'www.shaharuk.com'}))
    expires_at = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label="Expiration Date & Time ")
  