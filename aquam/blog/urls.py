from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from django.contrib import sitemaps
from .sitemaps import Detail
from . import views

sitemaps = {
    'detail': Detail,
}

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blog/(?P<current_paging_number>)(?P<category>)$', views.blog, name='blog'),
    url(r'^blog/(?P<current_paging_number>[0-9]+)(?P<category>)/$', views.blog),
    url(r'^blog/detail/(?P<board_number>[0-9]+)/$', views.blog_detail),
    url(r'^blog/(?P<category>[0-9]+)/(?P<current_paging_number>[0-9]+)/$', views.blog),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
]