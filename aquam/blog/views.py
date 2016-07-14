from django.shortcuts import render, redirect
from .models import Gallery, Image, Categorys
from django.core.paginator import Paginator
from django.shortcuts import render_to_response

from .forms import GallerySearchForm


# Create your views here.
def index(request):
    get_image_list = []
    for e in Categorys.objects.values('id'):
        get_gallery_per_categorys = Gallery.objects.order_by('-created_date').filter(categorys=e['id'])[:6]
        for f in get_gallery_per_categorys:
            try:
                get_image_list.append(Image.objects.order_by('-id').filter(gallery=f)[0])
            except:
                pass

    get_category = Categorys.objects.filter(gallery__images__isnull=False).distinct()
    get_gallery = Gallery.objects.filter(images__thumbnail=True, categorys__isnull=False)

    return render(request, 'cluster/index.html', {
        'image_list': get_image_list,
        'category_list': get_category,
        'gallery_list': get_gallery,
    })


def blog(request, current_paging_number, category):
    form = GallerySearchForm(request.GET)
    if current_paging_number == '':
        current_paging_number = '1'
    if category == '':
        page = Paginator(form.search().order_by('-created_date'), 5)
    else:
        try:
            if request.GET['q'] == '':
                page = Paginator(form.search().order_by('-created_date'), 5)
        except:
            page = Paginator(Gallery.objects.filter(categorys=category).order_by('-created_date'), 5)

    # 한번에 표시할 페이지 수
    page_count = 5
    # 최대 페이지 수
    page_max_count = page._get_num_pages()
    get_gallery = page
    get_image = Image.objects.filter(thumbnail='True')
    get_category = Categorys.objects.all()
    if (page_max_count-1) // page_count == (int(current_paging_number)-1) // page_count:
        page_loop = ((page_max_count-1) % page_count)+1
    else:
        page_loop = page_count
    return render(request, 'cluster/blog.html', {
        'blog_list': get_gallery.page(current_paging_number),
        'image_list': get_image,
        'paging_number': current_paging_number,
        'page_loop': page_loop,
        'page_size': page_count,
        'page_max_count': page_max_count,
        'category_list': get_category,
        'category': category,
    })


def blog_detail(request, board_number):
    if Gallery.objects.filter(id=board_number).count() != 0:
        get_blog_detail = Gallery.objects.filter(id=board_number)[0]
    else:
        return redirect('/blog/')
    get_image = Image.objects.filter(gallery=board_number)
    get_category = Categorys.objects.all()
    return render(request, 'cluster/blog_detail.html', {
        'board_number': board_number,
        'blog': get_blog_detail,
        'image_list': get_image,
        'category_list': get_category,
        'request': request,
    })