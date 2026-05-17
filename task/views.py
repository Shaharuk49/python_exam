from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
import uuid
from .forms import ShortenUrlForm
from .models import UrlData, ClickAnalytics
from django.utils import timezone

def index(request):
    short_url = None
    if request.method == 'POST':
        form = ShortenUrlForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['url']
            slug = str(uuid.uuid4())[:8]
            new_url = UrlData(url=original_url, slug=slug)
            new_url.save()
            expaires_at = form.cleaned_data.get('expires_at')
            if expaires_at: 
                new_url.expires_at = expaires_at
                new_url.save()
            short_url = f"{request.build_absolute_uri('/')}{slug}"
    else:
        form = ShortenUrlForm()
    return render(request, 'task/index.html', {'form': form, 'short_url': short_url})

def redirect_url(request, slug):
    url_data = get_object_or_404(UrlData, slug=slug)
    if url_data.expires_at and url_data.expires_at <= timezone.now():
        return render(request, 'task/expired.html')
    url_data.total_clicks = F('total_clicks') + 1
    url_data.save()
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown Agent')
    referrer = request.META.get('HTTP_REFERER', None)
    current_user = request.user if request.user.is_authenticated else None
    ClickAnalytics.objects.create(
        user=current_user,
        short_url=url_data,
        ip_address=ip,
        user_agent=user_agent,
        refer=referrer
    )
    return redirect(url_data.url)


def dashboard_view(request, slug=None):
    if slug:
      
        url_data = get_object_or_404(UrlData, slug=slug)
        recent_clicks = url_data.clicks.all().order_by('-timestamp')[:100]
        
        context = {
            'url_data': url_data,
            'recent_clicks': recent_clicks,
            'single_view': True,
        }
    else:
        
        all_urls = UrlData.objects.all().order_by('-time')
        
        context = {
            'all_urls': all_urls,
            'single_view': False,
        }
        
    return render(request, 'task/dashboard.html', context)
