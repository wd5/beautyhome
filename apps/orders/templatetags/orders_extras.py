# -*- coding: utf-8 -*-
from apps.products.models import Product
from apps.orders.models import Cart, OrderProduct, BuyLater
from apps.users.models import Profile
from django.db.models import Max, Count, Sum
from django import template
from pytils.numeral import choose_plural

register = template.Library()

@register.inclusion_tag("orders/block_cart.html", takes_context=True)
def block_cart(context):
    if 'request' in context:
        request = context['request']
        user = request.user

        cookies = request.COOKIES

        cookies_cart_id = False
        if 'beautyhome_cart_id' in cookies:
            cookies_cart_id = cookies['beautyhome_cart_id']

        if request.user.is_authenticated and request.user.id:
            profile_id = request.user.profile.id
        else:
            profile_id = False

        sessionid = request.session.session_key

        if profile_id:
            try:
                cart = Cart.objects.get(profile=profile_id)
            except Cart.DoesNotExist:
                if cookies_cart_id:
                    try:
                        cart = Cart.objects.get(id=cookies_cart_id)
                        if cart.profile:
                            cart = False
                        else:
                            try:
                                profile = Profile.objects.get(pk=int(profile_id))
                            except:
                                profile = False
                            if profile:
                                cart.profile = profile
                                cart.save()
                    except:
                        cart = False
                else:
                    cart = False
        elif cookies_cart_id:
            try:
                cart = Cart.objects.get(id=cookies_cart_id)
            except Cart.DoesNotExist:
                cart = False
        else:
            try:
                cart = Cart.objects.get(sessionid=sessionid)
            except Cart.DoesNotExist:
                cart = False
    else:
        cart = False
        user = False

    is_empty = True
    cart_total = 0
    cart_products_count = 0
    cart_products_text = u''
    if cart:
        cart_products_count = cart.get_products_count()
        if cart_products_count:
            cart_total = cart.get_str_total()
            is_empty = False
            cart_products_text = u'товар%s' % (choose_plural(cart_products_count, (u'', u'а', u'ов')))
    return {
        'is_empty': is_empty,
        'user': user,
        'cart_products_count': cart_products_count,
        'cart_total': cart_total,
        'cart_products_text': cart_products_text,
        }

@register.simple_tag()
def get_sum(cl):
    rl = cl.result_list
    sum = 0
    for order in rl:
        sum += order.get_total_summary()
    return sum


@register.inclusion_tag("orders/block_buy_later.html", takes_context=True)
def block_buy_later(context):
    if 'request' in context:
        request = context['request']

        if request.user.is_authenticated and request.user.id:
            profile_id = request.user.profile.id
        else:
            profile_id = False

        sessionid = request.session.session_key

        if profile_id:
            try:
                buy_later_cart = BuyLater.objects.get(profile=profile_id)
            except BuyLater.DoesNotExist:
                try:
                    buy_later_cart = BuyLater.objects.get(sessionid=sessionid)
                except BuyLater.DoesNotExist:
                    buy_later_cart = False
        else:
            try:
                buy_later_cart = BuyLater.objects.get(sessionid=sessionid)
            except BuyLater.DoesNotExist:
                buy_later_cart = False
    else:
        buy_later_cart = False

    products = False
    ids = ''

    if buy_later_cart:
        ids = buy_later_cart.product_ids
        if ids != '':
            ids_arr = ids.split(',')
            ids_arr = f7(ids_arr)
            products = Product.objects.published().filter(id__in=ids_arr)
            ids = ','.join(ids_arr)
            buy_later_cart.product_ids = ids
            buy_later_cart.save()

    return {
        'products': products,
        'ids': ids,
        }

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]
