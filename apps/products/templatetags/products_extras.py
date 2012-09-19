# -*- coding: utf-8 -*-
from apps.products.models import Category, Brand, Product
from django import template
from django.db.models import Q
from string import split

register = template.Library()

@register.simple_tag
def get_request_parameters(GET_PARAMS, empty_href, excl_param):
    str = ''
    for parameter in GET_PARAMS:
        if excl_param!=parameter:
            str = '%s&%s=%s' % (str, parameter, GET_PARAMS[parameter])

    if str.startswith('&') and empty_href=='True':
        str = '?%s' % str[1:]
    if not str.startswith('?') and empty_href=='True':
        str = '?%s' % str
    if str=='?':
        str = '#'
    return str

@register.inclusion_tag("products/block_all_footer_menu.html")
def block_all_footer_menu():
    categs_with_childs = []
    categs = []
    menu = Category.objects.filter(parent=None, is_published=True).select_related()
    for item in menu:
        childrens = item.children.filter(is_published=True, is_in_bottom_menu=True)
        if childrens:
            setattr(item, 'childrens', childrens)
            categs_with_childs.append(item)
        else:
            categs.append(item)
    return {'categs_with_childs': categs_with_childs, 'categs': categs}


@register.inclusion_tag("products/block_category_menu.html")
def block_category_menu(curr):
    if curr.startswith('/'):
        curr = curr[1:]
    if curr.endswith('/'):
        curr = curr[:-1]
    try:
        current_category = curr.split('/')[1]
    except:
        current_category = False
    menu = Category.objects.filter(parent=None, is_published=True)
    return {'menu': menu, 'current_category': current_category}


@register.inclusion_tag("products/block_brand_menu.html")
def block_brand_menu():
    brands = Brand.objects.published()
    return {'brands': brands}

@register.inclusion_tag("products/block_recent.html")
def block_recent(session):
    if 'recent_prod_ids' in session:
        products = Product.objects.filter(id__in=session['recent_prod_ids'][1:])
    else:
        products = False
    return {'products':products,'session':session['recent_prod_ids']}
