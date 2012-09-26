# -*- coding: utf-8 -*-
import os, md5
from datetime import datetime, date, timedelta
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Max, Min
from django.views.generic.base import TemplateView, View
from django.views.generic.simple import direct_to_template

from django.views.generic import ListView, DetailView, DetailView

from models import Category, Product, Brand, LECategory, LifeEvent, Review
from apps.faq.models import Advice



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
            if brands.count() == 0: brands = False

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
        if self.object.is_published == False:
            raise Http404
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
                if len(list) > 3:
                    list.pop(0)
                list.append(self.object.id)
            else:
                if len(list) > 3:
                    list.remove(self.object.id)
                list.append(self.object.id)
            self.request.session['recent_prod_ids'] = list
        else:
            self.request.session['recent_prod_ids'] = [self.object.id, ]
        return context

show_product = ShowProduct.as_view()

class ShowBrand(TemplateView):
    template_name = 'products/show_brand.html'

    def get_context_data(self, **kwargs):
        context = super(ShowBrand, self).get_context_data()
        slug = self.kwargs.get('slug', None)
        brands = Brand.objects.published()
        categories = Category.objects.filter(is_published=True)
        if slug == 'any': # если перешли по /brands/ - выведем любой
            try:
                brand = brands.order_by('?')[0]
            except:
                raise Http404
        else:
            try:
                brand = brands.get(slug=slug)
            except:
                raise Http404
        brand_cats_root = []
        brand_products = brand.get_products()

        cats = brand_products.values('category')
        cats_ids = [item['category'] for item in cats]
        parents_cats = categories.filter(parent=None)
        present = False
        for item in parents_cats:
            descendants = item.get_descendants(include_self=False)
            present = descendants.filter(id__in=cats_ids)
            products = brand_products.filter(category__id__in=present)[:7]
            if present:
                setattr(item, 'products', products)

        context['brand'] = brand
        context['brands'] = brands
        context['categories'] = parents_cats
        return context

show_brand = ShowBrand.as_view()

class ShowLifeEventView(TemplateView):
    template_name = 'products/show_life_event.html'

    def get_context_data(self, **kwargs):
        context = super(ShowLifeEventView, self).get_context_data()
        pk_1 = self.kwargs.get('pk_1', None)
        pk_2 = self.kwargs.get('pk_2', None)
        l_events = LifeEvent.objects.published()
        le_cats = LECategory.objects.published()
        if pk_1 == None:
            if pk_2 == None:
                try:
                    l_event = l_events.order_by('?')[0]
                    products = l_event.product_set.published()
                except:
                    raise Http404
            else:
                try:
                    l_event_cat = le_cats.get(id=pk_2)
                    l_event = l_event_cat.life_event
                    products = l_event_cat.product_set.published()
                    context['l_event_cat'] = l_event_cat
                except:
                    l_event = l_events.order_by('?')[0]
                    products = l_event.product_set.published()
        else:
            try:
                l_event = l_events.get(id=pk_1)
                products = l_event.product_set.published()
            except:
                raise Http404

        context['l_event'] = l_event
        context['l_events'] = l_events
        context['products'] = products[:15]
        return context

show_life_events = ShowLifeEventView.as_view()

class LoadLESubCat(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'selected_ids' not in request.POST:
                return HttpResponseBadRequest()

            id_category = request.POST['selected_ids']

            id_category_set = id_category.split(',')
            selecter_categs = False

            if id_category_set:
                selecter_categs = LifeEvent.objects.published().filter(id__in=id_category_set)

            html_code = u''
            if selecter_categs:
                for item in selecter_categs:
                    for subcat in item.get_sub_categories():
                        html_code = u'%s<option value="%s">%s - %s</option>' % (
                            html_code, subcat.id, item.title, subcat.title)

            return HttpResponse(html_code)
        else:
            return HttpResponseBadRequest()

load_le_subcat = LoadLESubCat.as_view()

class ReviewListView(ListView):
    model = Review
    template_name = 'products/reviews.html'
    context_object_name = 'reviews'
    queryset = model.objects.published()

show_reviews = ReviewListView.as_view()

class ShowReview(DetailView):
    model = Review
    context_object_name = 'review'
    template_name = 'products/show_review.html'

    def get_context_data(self, **kwargs):
        context = super(ShowReview, self).get_context_data()

        product = self.object.get_first_product()
        if product:
            category = product.category
            context['category'] = category
            context['parent_category'] = category.get_root()
            lvl = category.level
            if lvl == 3:
                context['sub_slug_3'] = category.slug
                context['sub_slug_2'] = category.parent.slug
                context['sub_slug_1'] = category.parent.parent.slug
                context['slug'] = category.parent.parent.parent.slug
            if lvl == 2:
                context['sub_slug_2'] = category.slug
                context['sub_slug_1'] = category.parent.slug
                context['slug'] = category.parent.parent.slug
            if lvl == 1:
                context['sub_slug_1'] = category.slug
                context['slug'] = category.parent.slug

        return context

show_review_detail = ShowReview.as_view()

class SearchInView(TemplateView):
    template_name = 'search_results.html'

    def get_context_data(self, **kwargs):
        context = super(SearchInView, self).get_context_data()
        products = Product.objects.published()
        advices = Advice.objects.published()
        reviews = Review.objects.published()
        brands = Brand.objects.published()
        try:
            q = self.request.GET['q']
        except:
            q = ''
        if q=='':
            q = '?'
        qs_products = products.filter(
            Q(title__icontains=q) |
            Q(category__title__icontains=q) |
            Q(brand__title__icontains=q) |
            Q(series__icontains=q) |
            Q(collection__icontains=q) |
            Q(art__icontains=q) |
            Q(composition__icontains=q) |
            Q(description__icontains=q) |
            Q(price__icontains=q)
        )
        qs_advices = advices.filter(
            Q(question__icontains=q) |
            Q(answer__icontains=q)
        )
        qs_reviews = reviews.filter(
            Q(title__icontains=q) |
            Q(short_description__icontains=q) |
            Q(description__icontains=q)
        )
        qs_brands = brands.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )
        context['result_products'] = qs_products
        context['result_advices'] = qs_advices
        context['result_reviews'] = qs_reviews
        context['result_brands'] = qs_brands
        context['query'] = q
        return context

search_in = SearchInView.as_view()