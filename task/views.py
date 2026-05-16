from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse # Added to show the error message
import uuid
from task.forms import ShortenUrlForm
from task.models import UrlData
from .forms import ShortenUrlForm   
from .models import UrlData





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
    return render(request, '/index.html', {'form': form, 'short_url': short_url})

@login_required
def dashboard_view(request):

    UrlData.objects.create(user=request.user, url_path=request.path)
    return render(request, 'task/dashboard.html')


@login_required
def tester_view(request):
    user_hits = UrlData.objects.filter(user=request.user).order_by('-timestamp')
    if user_hits.count() >= 3:
        
        return HttpResponse("You can't show this time", status=403,)
    
    UrlData.objects.create(user=request.user, url_path=request.path)
    
    return render(request, 'task/tester.html', {'tasks': user_hits})





def redirect_url(request, slug):
    url_details = UrlData.objects.get(slug=slug)
    return redirect(url_details.url)


def demo_view(request):
    return render(request, '/demo.html')    