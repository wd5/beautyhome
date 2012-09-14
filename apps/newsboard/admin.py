# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from apps.utils.widgets import Redactor
from models import News

class NewsAdminForm(forms.ModelForm):
    short_text = forms.CharField(
        widget=Redactor(attrs={'cols': 170, 'rows': 10}),
        label = u'Анонс',
    )
    text = forms.CharField(
        widget=Redactor(attrs={'cols': 170, 'rows': 30}),
        label = u'Текст',
    )
    class Meta:
        model = News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_add', 'is_published', )
    list_display_links = ('title',)
    list_filter = ('is_published',)
    form = NewsAdminForm
    date_hierarchy = 'date_add'

admin.site.register(News, NewsAdmin)
