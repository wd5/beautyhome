# -*- coding: utf-8 -*-
from apps.siteblocks.models import Settings
from django import template

register = template.Library()

@register.inclusion_tag("siteblocks/block_setting.html")
def block_static(name):
    try:
        setting = Settings.objects.get(name = name)
    except Settings.DoesNotExist:
        setting = False
    return {'block': block,}
