# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from apps.products.models import LifeEvent



class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['life_events'] = LifeEvent.objects.published()
        return context

index = IndexView.as_view()