from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blog/(?P<current_paging_number>)$', views.blog, name='blog'),
    url(r'^blog/(?P<current_paging_number>[0-9]+)/$', views.blog, name='blog'),
    url(r'^detail/(?P<board_number>[0-9]+)/$', views.blog_detail, name='blog'),
]