# -*- coding: utf-8 -*-
import os
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from pytils.translit import translify

from sorl.thumbnail import ImageField as sorl_ImageField
from apps.utils.managers import PublishedManager


class ImageField(sorl_ImageField, models.ImageField):
    pass

def file_path_News(instance, filename):
    return os.path.join('images','news',  translify(filename).replace(' ', '_') )

class News(models.Model):
    title = models.CharField(
        verbose_name = u'Заголовок',
        max_length = 250,
    )
    image = ImageField(
        verbose_name = u'Изображение',
        upload_to = file_path_News,
        blank = True,
    )
    short_text = models.TextField(
        verbose_name = u'Анонс',
    )
    text = models.TextField(
        verbose_name = u'Текст',
    )
    is_published = models.BooleanField(
        verbose_name = u'Опубликовано',
        default = True,
    )
    date_add = models.DateTimeField(
        verbose_name = u'Дата создания',
        default = datetime.now
    )
    # Managers
    objects = PublishedManager()

    class Meta:
        ordering = ['-date_add', '-id',]
        verbose_name =_(u'news_item')
        verbose_name_plural =_(u'news_items')
        get_latest_by = 'date_add'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return u'/news/%s/' % self.id