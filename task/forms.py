from django import forms


class ShortenUrlForm(forms.Form):
    url = forms.URLField(label="Enter your URL here", widget=forms.URLInput(attrs={'placeholder': 'www.shaharuk.com'}))