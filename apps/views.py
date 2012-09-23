# -*- coding: utf-8 -*-
from django.core.context_processors import csrf
from django.views.generic import TemplateView
from apps.products.models import LifeEvent, Product
from apps.siteblocks.models import Action
from apps.newsboard.models import News

class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['target'] = self.kwargs.get('target', None)
        context['life_events'] = LifeEvent.objects.published()
        context['news'] = News.objects.published()[:3]
        all_products = Product.objects.published()

        list_action_count = 2
        all_actions = Action.objects.published()
        context['actions'] = SplitQSItems(all_actions,list_action_count)

        list_product_count = 6
        context['products_daily'] = SplitQSItems(all_products.filter(is_daily=True),list_product_count)
        context['products_hit'] = SplitQSItems(all_products.filter(is_hit=True),list_product_count)
        context['products_new'] = SplitQSItems(all_products.filter(is_new=True),list_product_count)
        context['products_unique'] = SplitQSItems(all_products.filter(is_unique=True),list_product_count)
        context.update(csrf(self.request))
        return context

index = IndexView.as_view()

def SplitQSItems(QS, count):
    count = float(count)
    list = []
    counter = 0
    result_list = []
    for item in QS:
        counter += 1
        div = counter % count
        list.append(item)
        if div == 0:
            result_list.append(list)
            list = []
    if len(result_list)<QS.count()/count:
        result_list.append(list)
    return result_list