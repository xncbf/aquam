from django.shortcuts import render
from .models import Gallery, Image
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    return render(request, 'cluster/index.html', {

    })


def blog(request, current_paging_number):
    if current_paging_number == '':
        current_paging_number = '1'

    page = Paginator(Gallery.objects.order_by('-created_date'), 5)
    page_count = 4
    page_max_count = page._get_num_pages()
    get_gallery = page
    get_image = Image.objects.filter(thumbnail='True')
    if (page_max_count-1) // page_count == (int(current_paging_number)-1) // page_count:
        page_loop = page_max_count % page_count
    else:
        page_loop = page_count
    return render(request, 'cluster/blog.html', {
        'blog_list': get_gallery.page(current_paging_number),
        'image_list': get_image,
        'paging_number': current_paging_number,
        'page_loop': page_loop,
        'page_size': page_count,
        'page_max_count': page_max_count,
    })


def blog_detail(request, board_number):
    get_blog_detail = Gallery.objects.filter(id=board_number)[0]
    get_image = Image.objects.filter(gallery=board_number)
    return render(request, 'cluster/blog_detail.html', {
        'board_number': board_number,
        'blog': get_blog_detail,
        'image_list': get_image,
    })