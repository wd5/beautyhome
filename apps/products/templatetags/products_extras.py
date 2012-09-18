# -*- coding: utf-8 -*-
from apps.products.models import Category, Brand
from django import template
from django.db.models import Q
from string import split

register = template.Library()

@register.inclusion_tag("products/block_all_footer_menu.html")
def block_all_footer_menu():
    categs_with_childs = []
    categs = []
    menu = Category.objects.filter(parent=None, is_published=True)
    for item in menu:
        childrens = item.get_childs_in_menu()
        if childrens:
            setattr(item, 'childrens', childrens)
            categs_with_childs.append(item)
        else:
            categs.append(item)
    return {'categs_with_childs': categs_with_childs,'categs': categs}

@register.inclusion_tag("products/block_category_menu.html")
def block_category_menu():
    menu = Category.objects.filter(parent=None, is_published=True)
    return {'menu': menu}

@register.inclusion_tag("products/block_brand_menu.html")
def block_brand_menu():
    brands = Brand.objects.published()
    return {'brands': brands}
