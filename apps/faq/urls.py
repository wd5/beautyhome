# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from views import questions_list, show_question


urlpatterns = patterns('',

    url(r'^$',questions_list, name='questions_list'),
    (r'^(?P<pk>\d+)/$',show_question),
    #url(r'^sendquestion/$','apps.faq.views.question_form'),
    #url(r'^checkform/$','apps.faq.views.save_question_form'),

)