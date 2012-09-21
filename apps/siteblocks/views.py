# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView, DetailView

from models import Action

class ShowAction(DetailView):
    model = Action
    context_object_name = 'action'
    template_name = 'siteblocks/show_action.html'


show_action = ShowAction.as_view()