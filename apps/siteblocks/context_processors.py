# -*- coding: utf-8 -*-
from apps.siteblocks.models import Settings
from settings import SITE_NAME

def settings(request):
    try:
        phonenum = Settings.objects.get(name='phonenum').value
    except Settings.DoesNotExist:
        phonenum = False
    try:
        skype = Settings.objects.get(name='skype').value
    except Settings.DoesNotExist:
        skype = False
    try:
        vk = Settings.objects.get(name='vk').value
    except Settings.DoesNotExist:
        vk = False

    return {
        'phonenum': phonenum,
        'skype': skype,
        'vk': vk,
        'site_name': SITE_NAME,
    }