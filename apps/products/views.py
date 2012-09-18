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
            brand = int(self.request.GET['brand'])
        except:
            brand = False
        try:
            price_filter = int(self.request.GET['price_filter'])
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

        try:
            context['parent_category'] = all_categories.get(slug=slug)
        except:
            context['parent_category'] = False

        if category and category.count() == 1:
            category = category[0]
        elif category.count() > 1: # если по slug'у будет найдено несколько категорий
            try:
                category = category.get(parent__slug__in=[slug, sub_slug_1, sub_slug_2, sub_slug_3])
            except:
                category = False

        if category:
            context['category'] = category
            products = category.get_products()

            brands = Brand.objects.published().filter(id__in=products.values('brand__id')).values(
                'id', 'title')
            collection = products.values('collection').distinct().order_by('collection')
            series = products.values('series').distinct().order_by('series')
            color = products.values('color').distinct().order_by('color')
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

            if brand:
                products = products.filter(brand__id=brand)
                context['brand'] = brand

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

        # все указанные параметры товара
        product_features_values_set = self.object.get_feature_values()

        # группа с основными параметрами
        base_features_values = []
        base_feature_group = self.object.category.get_base_feature_group()
        for name in base_feature_group.get_feature_names():
            try:
                value = product_features_values_set.get(feature_name=name)
                base_features_values.append({'title': name.title, 'value': value})
            except:
                value = False
        setattr(base_feature_group, 'features_values', base_features_values)
        if base_features_values:
            context['base_feature_group'] = base_feature_group
        else:
            context['base_feature_group'] = False

        base_feature_group = self.object.category.get_base_feature_group()

        # группа с НЕосновными параметрами
        exists = False
        other_feature_groups = self.object.category.get_other_feature_groups()
        for gpoup in other_feature_groups:
            other_features_values = []
            for name in gpoup.get_feature_names():
                try:
                    value = product_features_values_set.get(feature_name=name)
                    exists = True
                    other_features_values.append({'title': name.title, 'value': value})
                except:
                    value = False
            setattr(gpoup, 'features_values', other_features_values)
        if exists:
            context['other_feature_groups'] = other_feature_groups
        else:
            context['other_feature_groups'] = []

        context['attached_photos'] = self.object.get_photos()

        # форма покупки "в один клик"
        product_qs = Product.objects.filter(id=self.object.id)
        try:
            mfrer = '%s - ' % self.object.brand.title
        except:
            mfrer = ''
        one_clk_form = OneClickByeForm(initial={'product': self.object,
                                                'product_description': u'%s%s %s' % (
                                                    mfrer, self.object.category.title_singular, self.object.title),
                                                'product_price': self.object.price})
        one_clk_form.fields['product'].queryset = product_qs
        context['one_clk_form'] = one_clk_form
        return context

show_product = ShowProduct.as_view()
