# -*- coding: utf-8 -*-
from apps.products.models import Review

def reviews(request):
    try:
        review_at_menu = Review.objects.published().latest()
    except Review.DoesNotExist:
        review_at_menu = False
    return {
        'review_at_menu': review_at_menu,
    }