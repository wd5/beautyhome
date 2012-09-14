# -*- coding: utf-8 -*-
import os, datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from apps.utils.managers import PublishedManager

from pytils.translit import translify
from django.core.urlresolvers import reverse

from sorl.thumbnail import ImageField
from mptt.models import MPTTModel, TreeForeignKey, TreeManager

def file_path_Brand(instance, filename):
    return os.path.join('images','brands',  translify(filename).replace(' ', '_') )
class Brand(models.Model):
    title = models.CharField(verbose_name=u'Название', max_length=255)
    image = ImageField(verbose_name=u'Изображение', upload_to=file_path_Brand, blank=True)
    description = models.TextField(verbose_name = u'Описание',)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    # Managers
    objects = PublishedManager()

    class Meta:
        verbose_name =_(u'brand')
        verbose_name_plural =_(u'brands')
        ordering = ['-order', 'title']

    def __unicode__(self):
        return self.title

    def get_products(self):
        return self.product_set.published()

def file_path_LifeEvent(instance, filename):
    return os.path.join('images','lifeEvents',  translify(filename).replace(' ', '_') )
class LifeEvent(models.Model):
    image = ImageField(verbose_name=u'Изображение', upload_to=file_path_LifeEvent, blank=True)
    title = models.CharField(verbose_name=u'Название', max_length=255)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    # Managers
    objects = PublishedManager()

    class Meta:
        verbose_name =_(u'life_event')
        verbose_name_plural =_(u'life_events')
        ordering = ['-order',]

    def __unicode__(self):
        return self.title

class Category(MPTTModel):
    parent = TreeForeignKey('self', verbose_name=u'Категория', related_name='children', blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(verbose_name=u'Название', max_length=100)
    slug = models.SlugField(verbose_name=u'Алиас', help_text=u'уникальное имя на латинице',)
    is_in_bottom_menu = models.BooleanField(verbose_name = u'Отображать в блоке "Всё сразу"', default=False, help_text=u'(только для категорий 2-го уровня)')
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    # Managers
    objects = TreeManager()

    def __unicode__(self):
            return self.title

    class Meta:
        verbose_name =_(u'category')
        verbose_name_plural =_(u'categories')
        ordering = ['-order', 'title']

    class MPTTMeta:
            order_insertion_by = ['order']


    def get_absolute_url(self):
        return u'' #self.alias

def str_price(price):
    if not price:
        return u'0'
    value = u'%s' %price
    if price._isinteger():
        value = u'%s' %value[:len(value)-3]
        count = 3
    else:
        count = 6

    if len(value)>count:
        ends = value[len(value)-count:]
        starts = value[:len(value)-count]

        return u'%s %s' %(starts, ends)
    else:
        return value

def file_path_Product(instance, filename):
    return os.path.join('images','products',  translify(filename).replace(' ', '_') )
class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'Категория')
    brand = models.ForeignKey(Brand, verbose_name=u'Брэнд', blank=True, null=True)
    title = models.CharField(verbose_name=u'Название', max_length=400)
    image = ImageField(verbose_name=u'Изображение', upload_to=file_path_Product)

    series = models.CharField(verbose_name=u'Серия', max_length=100, blank=True)
    collection = models.CharField(verbose_name=u'Коллекция', max_length=100, blank=True)
    art = models.CharField(verbose_name=u'Артикул', max_length=50, blank=True)
    color = models.CharField(verbose_name = u'Цвет', max_length=50, blank=True)
    volume = models.CharField(verbose_name = u'Объем', max_length=20, blank=True)

    price = models.DecimalField(verbose_name=u'Цена', decimal_places=2, max_digits=10,)
    old_price = models.DecimalField(verbose_name=u'Старая цена', decimal_places=2, max_digits=10, blank=True, null=True)

    description = models.TextField(verbose_name=u'Описание',)
    application = models.TextField(verbose_name=u'Способ применения',)
    composition = models.TextField(verbose_name=u'Состав',)

    discount = models.CharField(verbose_name = u'Скидка/Акция', max_length=10, blank=True)
    discount_present = models.BooleanField(verbose_name=u'Подарок', default=False)
    discount_description = models.TextField(verbose_name=u'Описание Скидки/Акции', blank=True)

    is_new = models.BooleanField(verbose_name=u'Новинка', default=False)
    is_hit = models.BooleanField(verbose_name=u'Хит продаж', default=False)
    is_daily = models.BooleanField(verbose_name=u'Товар дня', default=False)
    is_unique = models.BooleanField(verbose_name=u'Уникальный товар', default=False)
    is_limit = models.BooleanField(verbose_name=u'Limited Edition', default=False)

    life_events = models.ManyToManyField(LifeEvent, verbose_name=u'для случаев жизни', blank=True, null=True)
    related_products = models.ManyToManyField("self", verbose_name=u'С этим товаром рекомендуем купить', blank=True, null=True,)

    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)

    # Managers
    objects = PublishedManager()

    class Meta:
        verbose_name =_(u'product_item')
        verbose_name_plural =_(u'product_items')
        ordering = ['-order', 'title']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products_detail',kwargs={'pk': '%s'%self.id})

    def get_str_price(self):
        return str_price(self.price)

    def get_str_old_price(self):
        return str_price(self.old_price)

    def get_photos(self):
        return self.photo_set.all()

def file_path_Product(instance, filename):
     return os.path.join('images','products',  translify(filename).replace(' ', '_') )
class Photo(models.Model):
    product = models.ForeignKey(Product, verbose_name=u'Товар')
    image = ImageField(verbose_name=u'Изображение', upload_to=file_path_Product)
    order = models.IntegerField(verbose_name=u'Порядок сортировки',default=10)

    class Meta:
        verbose_name =_(u'product_photo')
        verbose_name_plural =_(u'product_photos')
        ordering = ['-order',]

    def __unicode__(self):
        return u'Фото товара %s' %self.product.name

class Review(models.Model):
    title = models.CharField(verbose_name=u'Название', max_length=255)
    date_create = models.DateTimeField(verbose_name = u'Дата', default=datetime.datetime.now)
    description = models.TextField(verbose_name = u'Текст обзора',)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=True)
    products = models.ManyToManyField(Product, verbose_name=u'товары обзора', blank=True, null=True)

    # Managers
    objects = PublishedManager()

    class Meta:
        verbose_name =_(u'review')
        verbose_name_plural =_(u'reviews')
        ordering = ['-date_create',]

    def __unicode__(self):
        return self.title