# -*- coding: utf-8 -*-
DATABASE_NAME = u'beautyhome'
PROJECT_NAME = u'beautyhome'
SITE_NAME = u'Beauty Home'
DEFAULT_FROM_EMAIL = u'support@beautyhome.octweb.ru'

from config.base import *

try:
    from config.development import *
except ImportError:
    from config.production import *

TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += (
    'apps.siteblocks',
    'apps.pages',
    'apps.faq',
    'apps.products',
    'apps.newsboard',
    'apps.users',
    'apps.orders',
    #'apps.spam',



    'sorl.thumbnail',
    #'south',
    #'captcha',
)

MIDDLEWARE_CLASSES += (
    'apps.pages.middleware.PageFallbackMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'apps.pages.context_processors.meta',
    'apps.siteblocks.context_processors.settings',
    'apps.utils.context_processors.authorization_form',
)

#from settings_DebugToolbar import *