# -*- coding: utf-8 -*-
from apps.siteblocks.models import Settings, Banner
from django import template

register = template.Library()

@register.inclusion_tag("siteblocks/block_setting.html")
def block_static(name):
    try:
        setting = Settings.objects.get(name=name)
    except Settings.DoesNotExist:
        setting = False
    return {'block': block, }


@register.inclusion_tag("siteblocks/block_banner.html")
def block_banner():
    banner = Banner.objects.published()
    try:
        banner = banner.order_by("?")[:1]
    except:
        banner = False
    return {'banner': banner, }
