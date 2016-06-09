from django.shortcuts import render
from blog.models import Gallery

# Create your views here.
def index(request):
    return render(request, 'cluster/index.html', {

    })

def blog(request):
    for e in Gallery.detail.all():
        print(e.headline)
    return render(request, 'cluster/blog.html', {

    })
