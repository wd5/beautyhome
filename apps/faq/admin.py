# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Question, Advice

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','pub_date','name','email', 'is_published',)
    list_display_links = ('id','pub_date',)
    list_editable = ('is_published',)
    search_fields = ('name','email', 'question', 'answer',)
    list_filter = ('is_published','pub_date',)

admin.site.register(Question, QuestionAdmin)

class AdviceAdmin(admin.ModelAdmin):
    list_display = ('id','pub_date','name','email', 'is_published',)
    list_display_links = ('id','pub_date',)
    list_editable = ('is_published',)
    search_fields = ('name','email', 'question', 'answer',)
    list_filter = ('is_published','pub_date',)

admin.site.register(Advice, AdviceAdmin)