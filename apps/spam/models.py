# -*- coding: utf-8 -*-
import os, datetime
from django.db import models

class Mailer(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=100)
    pub_date = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'Дата')
    text = models.TextField(verbose_name=u'Текст')

    class Meta:
        verbose_name = u'рассылка'
        verbose_name_plural = u'рассылки'
        ordering = ('-pub_date',)

    def __unicode__(self):
        return self.name

    # todo: emailы буду брать из модели пользователей проверяя галочку "подписка"