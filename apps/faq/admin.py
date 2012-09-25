# -*- coding: utf-8 -*-Описание
from django.contrib import admin
from django import forms
from apps.utils.widgets import Redactor
from sorl.thumbnail.admin import AdminImageMixin
from models import Question, Advice

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','name','pub_date', 'is_published',)
    list_display_links = ('id','name','pub_date',)
    list_editable = ('is_published',)
    search_fields = ('question','name', 'answer',)
    list_filter = ('is_published','pub_date',)

admin.site.register(Question, QuestionAdmin)


class AdviceAdminForm(forms.ModelForm):
    answer = forms.CharField(widget=Redactor(attrs={'cols': 110, 'rows': 20}), required=False)
    answer.label=u'Ответ'

    class Meta:
        model = Advice

class AdviceAdmin(admin.ModelAdmin):
    list_display = ('id','name','pub_date','is_published',)
    list_display_links = ('id','name','pub_date',)
    list_editable = ('is_published',)
    search_fields = ('question', 'name', 'answer',)
    list_filter = ('is_published','pub_date',)
    form = AdviceAdminForm

admin.site.register(Advice, AdviceAdmin)