# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from datetime import date, datetime, timedelta
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from apps.users.views import GetLoadIds

from models import News

class NewsListView(TemplateView):
    template_name = 'newsboard/news_list.html'
    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data()
        news = News.objects.published()
        loaded_count = 5
        result = GetLoadIds(news, loaded_count, True)
        splited_result = result.split('!')
        try:
            remaining_count = int(splited_result[0])
        except:
            remaining_count = False
        next_id_loaded_items = splited_result[1]
        context['loaded_count'] = remaining_count
        context['next_id_loaded_items'] = next_id_loaded_items
        context['news'] = news[:loaded_count]
        return context

news_list = NewsListView.as_view()


class NewsDetailView(DetailView):
    context_object_name = 'news_current'
    model = News
    queryset = model.objects.published()
    template_name = 'newsboard/detail.html'

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs.get('pk', None)
        try:
            obj = queryset.get(pk=pk)
        except ObjectDoesNotExist:
            return False
        return obj

    def get(self, request, **kwargs):
        self.object = self.get_object()
        if not self.object:
            return HttpResponseRedirect(reverse('news_list'))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

news_detail = NewsDetailView.as_view()


class LatestNewsFeed(Feed):
    title = u'Новости'
    link = '/news/'
    description = ''

    def items(self):
        return News.objects.published()[:50]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_text