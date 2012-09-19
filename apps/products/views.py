# -*- coding: utf-8 -*-
import os, md5
from datetime import datetime, date, timedelta
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Max, Min
from django.views.generic.base import TemplateView
from django.views.generic.simple import direct_to_template

from django.views.generic import ListView, DetailView, DetailView

from models import Category, Product, Brand


class ShowCategory(TemplateView):
    template_name = 'products/show_category.html'

    def get_context_data(self, **kwargs):
        context = super(ShowCategory, self).get_context_data()

        try:
            brand = self.request.GET['brand']
        except:
            brand = False
        try:
            collection_value = self.request.GET['collection']
        except:
            collection_value = False
        try:
            series_value = self.request.GET['series']
        except:
            series_value = False
        try:
            color_value = self.request.GET['color']
        except:
            color_value = False
        try:
            price_filter = self.request.GET['price_filter']
        except:
            price_filter = False

        context['slug'] = slug = self.kwargs.get('slug', None)
        context['sub_slug_1'] = sub_slug_1 = self.kwargs.get('sub_slug_1', None)
        context['sub_slug_2'] = sub_slug_2 = self.kwargs.get('sub_slug_2', None)
        context['sub_slug_3'] = sub_slug_3 = self.kwargs.get('sub_slug_3', None)

        all_categories = Category.objects.filter(is_published=True)
        category = False
        if slug or sub_slug_1 or sub_slug_2 or sub_slug_3:
            if sub_slug_3:
                try:
                    category = all_categories.filter(slug=sub_slug_3)
                except:
                    pass
            if sub_slug_2 and not category:
                try:
                    category = all_categories.filter(slug=sub_slug_2)
                except:
                    pass
            if sub_slug_1 and not category:
                try:
                    category = all_categories.filter(slug=sub_slug_1)
                except:
                    pass
            if slug and not category:
                try:
                    category = all_categories.filter(slug=slug)
                except:
                    pass
        else:
            category = False

        if category and category.count() == 1:
            category = category[0]
        elif category.count() > 1: # если по slug'у будет найдено несколько категорий
            try:
                category = category.get(parent__slug__in=[slug, sub_slug_1, sub_slug_2, sub_slug_3])
            except:
                category = False

        if category:
            context['parent_category'] = category.get_root()
            context['category'] = category
            products = category.get_products()

            brands = Brand.objects.published().filter(id__in=products.values('brand__id')).values(
                'id', 'title')

            if brand:
                products = products.filter(brand__title__exact=brand)
                context['brand'] = brand

            collection = products.values('collection').exclude(collection__exact='').distinct().order_by('collection')
            series = products.values('series').exclude(series__exact='').distinct().order_by('series')
            color = products.values('color').exclude(color__exact='').distinct().order_by('color')
            if brands.count()==0: brands = False

            setattr(context['category'], 'brands', brands)
            setattr(context['category'], 'collection', collection)
            setattr(context['category'], 'series', series)
            setattr(context['category'], 'color', color)
            dic = products.aggregate(Min('price'), Max('price'))
            context['max_price'] = dic['price__max']
            context['min_price'] = dic['price__min']
            if context['max_price'] == None:
                context['max_price'] = 0
                context['min_price'] = 0

            if collection_value:
                products = products.filter(collection__exact=collection_value)
                context['collection_value'] = collection_value
            if series_value:
                products = products.filter(series__exact=series_value)
                context['series_value'] = series_value
            if color_value:
                products = products.filter(color__exact=color_value)
                context['color_value'] = color_value

            if price_filter:
                products = products.filter(price__lte=price_filter)
                context['price_filter'] = price_filter

            context['catalog'] = products
        else:
            context['category'] = False
        return context

show_category = ShowCategory.as_view()

class ShowProduct(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/show_product.html'

    def get_context_data(self, **kwargs):
        context = super(ShowProduct, self).get_context_data()
        context['slug'] = slug = self.kwargs.get('slug', None)
        context['sub_slug_1'] = sub_slug_1 = self.kwargs.get('sub_slug_1', None)
        context['sub_slug_2'] = sub_slug_2 = self.kwargs.get('sub_slug_2', None)
        context['sub_slug_3'] = sub_slug_3 = self.kwargs.get('sub_slug_3', None)

        category = self.object.category
        context['category'] = category
        context['parent_category'] = category.get_root()
        context['attached_photos'] = self.object.get_photos()

        # недавно просмотренные:
        if 'recent_prod_ids' in self.request.session:
            list = self.request.session['recent_prod_ids']
            if self.object.id not in list:
                if len(list)>3:
                    list.pop(0)
                list.append(self.object.id)
            else:
                if len(list)>3:
                    list.remove(self.object.id)
                list.append(self.object.id)
            self.request.session['recent_prod_ids'] = list
        else:
            self.request.session['recent_prod_ids'] = [self.object.id,]
        return context

show_product = ShowProduct.as_view()
