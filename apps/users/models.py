# -*- coding: utf-8 -*-
import os, datetime, settings
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

sex_choices = (
    (u'male', u'Мужской'),
    (u'female', u'Женский'),
)

class Profile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100, verbose_name=u'Имя')
    last_name = models.CharField(max_length=100, verbose_name=u'фамилия')
    third_name = models.CharField(max_length=100, verbose_name=u'отчество')
    phone = models.CharField(max_length=50, verbose_name=u'телефон', blank=True)
    b_day = models.DateField(verbose_name=u'дата рождения',)
    sex = models.CharField(max_length=30, verbose_name=u'Пол', choices=sex_choices, )
    is_in_subscribe = models.BooleanField(verbose_name=u'подписка на рассылку новостей', default=False)

    class Meta:
        verbose_name =_(u'user_profile')
        verbose_name_plural =_(u'users_profiles')

    def __unicode__(self):
        return u'%s' % self.user.username

    def get_name(self):
        if self.name:
            return u'%s' % self.name
        else:
            return u'нет имени'

    def get_orders(self):
        return self.order_set.all()

class ProfileAddress(models.Model):
    user = models.OneToOneField(User)
    city = models.CharField(max_length=255, verbose_name=u'Адрес')
    street = models.CharField(max_length=255, verbose_name=u'Улица, Дом, Квартира')

    class Meta:
        verbose_name =_(u'profile_addres')
        verbose_name_plural =_(u'profile_addreses')

    def __unicode__(self):
        return u'%s %s' % (self.city, self.street)