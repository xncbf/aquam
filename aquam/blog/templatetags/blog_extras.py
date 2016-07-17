from django import template
from django.conf import settings
import re

register = template.Library()
page_size = 5


@register.filter
def paging(value):
    currunt_page = int(value)
    page = (currunt_page-1)//page_size
    return page*page_size


@register.filter
def currunt_active(value, arg):
    page = int(arg) % page_size
    str1 = ''
    if int(value) % page_size == page:
        str1 = 'class=active'
    return str1


@register.filter
def get_range(value):
    return range(value)


@register.filter
def string_to_image(value, arg):
    pattern = re.compile(r"({\d+})")
    for (numbers) in re.findall(pattern, value):
        if int(re.sub(r'\D', '', numbers)) >= arg.count():
            break
        value = value.replace(numbers,
                               '<img class="img-responsive" src="' +
                               settings.MEDIA_URL +
                               'images/' +
                               arg[int(re.sub(r'\D', '', numbers))].filename +
                               '" alt="">')
    result = value
    return result


@register.filter
def string_to_blank(value):
    pattern = re.compile(r"({\d+})")
    result = pattern.sub("", value)
    return result


@register.filter
def lookup(d, key):
    return d[key]


@register.filter
def string_to_int(value):
    return int(value)
