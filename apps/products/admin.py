# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django import forms
from apps.utils.widgets import Redactor
from sorl.thumbnail.admin import AdminImageMixin
from mptt.admin import MPTTModelAdmin


from models import *

class CategoryAdmin(AdminImageMixin, MPTTModelAdmin):
    list_display = ('id','title','parent','slug','order','is_published',)
    list_display_links = ('id','title',)
    list_editable = ('order','is_published',)

admin.site.register(Category, CategoryAdmin)

class PhotoInline(admin.TabularInline):
    model = Photo
#--Виджеты jquery Редактора
class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=Redactor(attrs={'cols': 110, 'rows': 20}), required=False)
    description.label=u'Описание'

    full_description = forms.CharField(widget=Redactor(attrs={'cols': 110, 'rows': 20}), required=False)
    full_description.label=u'Полное описание'

    class Meta:
        model = Product
#--Виджеты jquery Редактора
class ProductAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id','title', 'category','price','old_price','order','is_published',)
    list_display_links = ('id','title',)
    list_editable = ('order','is_published',)
    list_filter = ('is_published','is_hit','is_new','is_daily','is_unique','is_limit',)
    search_fields = ('title', 'description', 'application', 'composition',)
    inlines = [PhotoInline]
    form = ProductAdminForm

admin.site.register(Product, ProductAdmin)