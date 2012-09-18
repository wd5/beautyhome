# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django import forms
from apps.utils.widgets import Redactor
from sorl.thumbnail.admin import AdminImageMixin
from mptt.admin import MPTTModelAdmin
from apps.utils.customfilterspec import CustomFilterSpec


from models import *

class BrandAdminForm(forms.ModelForm):
    description = forms.CharField(widget=Redactor(attrs={'cols': 110, 'rows': 20}), required=True)
    description.label=u'Описание'

    class Meta:
        model = Brand

    class Media:
        js = (
            '/media/js/jquery.js',
            '/media/js/clientadmin.js',
            '/media/js/jquery.synctranslit.js',
            )

class BrandAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','title','order','is_published',)
    list_display_links = ('id','title',)
    list_editable = ('order','is_published',)
    list_filter = ('is_published',)
    search_fields = ('title', 'description',)
    form = BrandAdminForm

admin.site.register(Brand, BrandAdmin)

class LifeEventAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','title','order','is_published',)
    list_display_links = ('id','title',)
    list_editable = ('order','is_published',)
    list_filter = ('is_published',)
    search_fields = ('title',)

admin.site.register(LifeEvent, LifeEventAdmin)

class CategoryAdminForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Category.objects.filter(level__lt=3), label='Родительская Категория', required=True)

    class Meta:
        model = Category

    class Media:
        js = (
            '/media/js/jquery.js',
            '/media/js/clientadmin.js',
            '/media/js/jquery.synctranslit.js',
            )

class CategoryAdmin(AdminImageMixin, MPTTModelAdmin):
    list_display = ('id','title','parent','slug','order','is_published',)
    list_display_links = ('id','title',)
    list_editable = ('order','is_published',)
    search_fields = ('title','slug',)
    form = CategoryAdminForm
    list_filter = ('is_published','parent',)
    custom_filter_spec = {'parent': Category.objects.filter(level__lt=3)}

admin.site.register(Category, CategoryAdmin)

class PhotoInline(AdminImageMixin, admin.TabularInline):
    model = Photo

class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=Redactor(attrs={'cols': 110, 'rows': 10}), required=False)
    description.label=u'Описание'
    application = forms.CharField(widget=Redactor(attrs={'cols': 110, 'rows': 10}), required=False)
    application.label=u'Применение'
    composition = forms.CharField(widget=Redactor(attrs={'cols': 110, 'rows': 10}), required=False)
    composition.label=u'Состав'
    discount_description = forms.CharField(widget=Redactor(attrs={'cols': 110, 'rows': 20}), required=False)
    discount_description.label=u'Описание Скидки/Акции'

    class Meta:
        model = Product

field_set = (
        (None, {
            'fields': ('category', 'brand', 'title','image')
        }),
        ('Параметры', {
            'classes': ('collapse',),
            'fields': ('series', 'collection', 'art','color','volume',)
        }),
        ('Цена', {
            'fields': ('price', 'old_price')
        }),
        ('Описание', {
            'classes': ('collapse',),
            'fields': ('description', 'application','composition',)
        }),
        ('Скидка/Акция', {
            'classes': ('collapse',),
            'fields': ('discount','discount_present','discount_description',)
        }),
        ('Свойства', {
            'classes': ('collapse',),
            'fields': ('is_new','is_hit','is_daily','is_unique','is_limit',)
        }),
        (None, {
            'fields': ('life_events','related_products','order','is_published',)
        }),
    )

class ProductAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','title', 'category','price','order','is_published',)
    list_display_links = ('id','title',)
    list_editable = ('order','is_published',)
    list_filter = ('is_published','is_hit','is_new','is_daily','is_unique','is_limit','color','category')
    search_fields = ('title', 'brand', 'series', 'collection', 'art', 'color', 'volume', 'description', 'application', 'composition',)
    raw_id_fields = ('related_products',)
    fieldsets = field_set
    inlines = [PhotoInline]
    form = ProductAdminForm

admin.site.register(Product, ProductAdmin)