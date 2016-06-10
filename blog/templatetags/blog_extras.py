from django import template

register = template.Library()
page_size = 4


@register.filter
def paging(value):
    currunt_page = int(value)
    page = (currunt_page-1)//page_size
    return page*page_size


@register.filter
def currunt_active(value, arg):
    """
    :param value:
    :param arg:
    :return:
    """
    page = int(arg) % page_size
    str1 = ''
    if int(value) % page_size == page:
        str1 = 'class=active'
    return str1


@register.filter
def get_range(value):
    return range(value)
