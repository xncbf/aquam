# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import scrapy_djangoitem
from scrapy_djangoitem import DjangoItem
from blog.models import Gallery,Image,Categorys

class NaverScraperItem(DjangoItem):
    django_model = Gallery
