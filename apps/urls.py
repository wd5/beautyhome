# -*- coding: utf-8 -*-
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from apps.products.views import show_category, show_product, show_brand, load_le_subcat, show_life_events, show_reviews, show_review_detail, search_in
from apps.orders.views import show_order_info
from apps.newsboard.views import news_list,news_detail
from apps.siteblocks.views import show_action
from django.conf.urls.defaults import patterns, include, url
from apps.users.views import show_cabinet, edt_profile_info, show_profile_form, registration_form, items_loader, check_addr_modal, del_addr

#from apps.app.urls import urlpatterns as app_url

from views import index

#url(r'^captcha/', include('captcha.urls')),
urlpatterns = patterns('',
    url(r'^$',index, name='index'),
    (r'^faq/', include('apps.faq.urls')),
    (r'^visage_advices/(?P<pk>\d+)/$','apps.faq.views.show_advice'),
    (r'^visage_advices/', 'apps.faq.views.show_visage_advices'),
    (r'^load_items/$',csrf_exempt(items_loader)),

    (r'^actions/(?P<pk>\d+)/$',show_action),
    (r'^actions/$',index, {'target':'actions'}),

    (r'^news/(?P<pk>\d+)/$',news_detail),
    (r'^news/$',news_list),

    (r'^brands/$',show_brand, {'slug':'any'}),
    (r'^brands/(?P<slug>[^/]+)/$',show_brand),

    (r'^lifeevents/$',show_life_events),
    (r'^lifeevents/(?P<pk_1>\d+)/$',show_life_events),
    (r'^lifeevents/[^/]+/(?P<pk_2>\d+)/$',show_life_events),

    (r'^load_le_subcat/$',csrf_exempt(load_le_subcat)),

    (r'^reviews/$',show_reviews),
    (r'^reviews/(?P<pk>\d+)/$',show_review_detail),

    (r'^search/$',search_in),

    (r'^category/$', index),
    (r'^category/(?P<slug>[^/]+)/$',show_category, {'sub_slug':'all'}),
    (r'^category/(?P<slug>[^/]+)/(?P<pk>\d+)/$',show_product),

    (r'^category/(?P<slug>[^/]+)/(?P<sub_slug_1>[^/]+)/$',show_category),
    (r'^category/(?P<slug>[^/]+)/(?P<sub_slug_1>[^/]+)/(?P<pk>\d+)/$',show_product),

    (r'^category/(?P<slug>[^/]+)/(?P<sub_slug_1>[^/]+)/(?P<sub_slug_2>[^/]+)/$',show_category),
    (r'^category/(?P<slug>[^/]+)/(?P<sub_slug_1>[^/]+)/(?P<sub_slug_2>[^/]+)/(?P<pk>\d+)/$',show_product),

    (r'^category/(?P<slug>[^/]+)/(?P<sub_slug_1>[^/]+)/(?P<sub_slug_2>[^/]+)/(?P<sub_slug_3>[^/]+)/$',show_category),
    (r'^category/(?P<slug>[^/]+)/(?P<sub_slug_1>[^/]+)/(?P<sub_slug_2>[^/]+)/(?P<sub_slug_3>[^/]+)/(?P<pk>\d+)/$',show_product),

    url(r'^cabinet/$',show_cabinet, {'division':'history'}, name='show_cabinet'),
    url(r'^cabinet/history/$',show_cabinet, {'division':'history'}),
    url(r'^cabinet/history/order/(?P<pk>\d+)/$',show_order_info),
    url(r'^cabinet/info/$',show_cabinet, {'division':'info'}),
    url(r'^cabinet/addresses/$',show_cabinet, {'division':'addresses'}),
    url(r'^cabinet/bonus/$',show_cabinet, {'division':'bonus'}),

    (r'^cabinet/edit_info_form/$',show_profile_form),
    (r'^cabinet/check_addr_modal/$',check_addr_modal),
    (r'^cabinet/del_addr/$',del_addr),
    (r'^edt_profile_info/$',edt_profile_info),
    (r'^registration_form/$',registration_form),
    url(r'^password/reset/$',
        auth_views.password_reset,
            {'template_name': 'users/password_reset_form.html',},
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
            {'template_name': 'users/password_reset_confirm.html'},
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
            {'template_name': 'users/password_reset_complete.html'},
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
            {'template_name': 'users/password_reset_done.html'},
        name='auth_password_reset_done'),
    url(r'^password/change/$',
        auth_views.password_change,
            {'template_name': 'users/password_change_form.html'},
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
            {'template_name': 'users/password_change_done.html'},
        name='auth_password_change_done'),

    url(r'^cart/$','apps.orders.views.view_cart',name='cart'),
    (r'^add_product_to_cart/$','apps.orders.views.add_product_to_cart'),
    (r'^delete_product_from_cart/$','apps.orders.views.delete_product_from_cart'),
    (r'^restore_product_to_cart/$','apps.orders.views.restore_product_to_cart'),
    (r'^change_cart_product_count/$','apps.orders.views.change_cart_product_count'),
    (r'^set_product_later_from_cart/$','apps.orders.views.set_product_later_from_cart'),
    (r'^get_later_list/$','apps.orders.views.get_later_list'),
    (r'^get_cartbox_html/$','apps.orders.views.get_cartbox_html'),
    (r'^get_cartin_html/$','apps.orders.views.get_cartin_html'),
    (r'^show_order_form/$','apps.orders.views.show_order_form'),
    (r'^order_form_step2/$','apps.orders.views.show_finish_form'),


)

#urlpatterns += #app_url


