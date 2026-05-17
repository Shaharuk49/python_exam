from django.shortcuts import render, redirect, get_object_or_404
import uuid
from .forms import ShortenUrlForm
from .models import UrlData, ClickAnalytics
from django.db.models import Count

def index(request):
    short_url = None
    if request.method == 'POST':
        form = ShortenUrlForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['url']
            slug = str(uuid.uuid4())[:8]
            new_url = UrlData(url=original_url, slug=slug)
            new_url.save()
            short_url = f"{request.build_absolute_uri('/')}{slug}"
    else:
        form = ShortenUrlForm()
    return render(request, 'task/index.html', {'form': form, 'short_url': short_url})

def redirect_url(request, slug):
    short_url_obj = get_object_or_404(UrlData, slug=slug)
    return redirect(short_url_obj.url)


def redirect_and_track(request, slug):
  
    short_url_obj = get_object_or_404(UrlData, slug=slug)
    ip_address = request.META.get('REMOTE_ADDR')
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        ip = x_forwarded.split(',')[0]
    else:
        ip = ip_address

    
    agent = request.META.get('HTTP_USER_AGENT', '')
    referer = request.META.get('HTTP_REFERER', '') 
 
    ClickAnalytics.objects.create(
        short_url=short_url_obj,
        ip_address=ip,
        user_agent=agent,
        refer=referer
    )
    
    return redirect(short_url_obj.url)

# def dashboard_view(request):
#     urls = UrlData.objects.all()
#     clicks = ClickAnalytics.objects.all()
#     return render(request, 'task/dashboard.html', {'urls': urls, 'clicks': clicks})


from django.db.models import Count

def dashboard_view(request):
    urls = UrlData.objects.annotate(total_clicks=Count('clicks'))
    return render(request, 'task/dashboard.html', {'urls': urls})

