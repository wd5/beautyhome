# -*- coding: utf-8 -*-
from apps.faq.models import Question, Advice

def faq(request):
    try:
        question_at_menu = Question.objects.published().latest()
    except Question.DoesNotExist:
        question_at_menu = False
    return {
        'question_at_menu': question_at_menu,
    }

def advice(request):
    try:
        advice_at_menu = Advice.objects.published().latest()
    except Advice.DoesNotExist:
        advice_at_menu = False
    return {
        'advice_at_menu': advice_at_menu,
    }