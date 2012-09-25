# -*- coding: utf-8 -*-
from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from models import Question, Advice

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','name','pub_date', 'is_published',)
    list_display_links = ('id','name','pub_date',)
    list_editable = ('is_published',)
    search_fields = ('question','name', 'answer',)
    list_filter = ('is_published','pub_date',)

admin.site.register(Question, QuestionAdmin)

class AdviceAdmin(admin.ModelAdmin):
    list_display = ('id','name','pub_date','is_published',)
    list_display_links = ('id','name','pub_date',)
    list_editable = ('is_published',)
    search_fields = ('question', 'name', 'answer',)
    list_filter = ('is_published','pub_date',)

admin.site.register(Advice, AdviceAdmin)