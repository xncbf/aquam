from django.shortcuts import render
from .models import Gallery, Image, Categorys
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    get_image = Image.objects.filter(thumbnail=True, gallery__categorys__isnull=False)
    get_category = Categorys.objects.all()
    get_gallery = Gallery.objects.filter(images__thumbnail=True, categorys__isnull=False)

    return render(request, 'cluster/index.html', {
        'image_list': get_image,
        'category_list': get_category,
        'gallery_list': get_gallery,
    })


def blog(request, current_paging_number, category):
    if current_paging_number == '':
        current_paging_number = '1'
    if category == '':
        page = Paginator(Gallery.objects.order_by('-created_date'), 5)
    else:
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
    get_blog_detail = Gallery.objects.filter(id=board_number)[0]
    get_image = Image.objects.filter(gallery=board_number)
    get_category = Categorys.objects.all()
    return render(request, 'cluster/blog_detail.html', {
        'board_number': board_number,
        'blog': get_blog_detail,
        'image_list': get_image,
        'category_list': get_category,
    })