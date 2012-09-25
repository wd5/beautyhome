# -*- coding: utf-8 -*-
from django.core.mail.message import EmailMessage
from django.db import models
import datetime, settings, os
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from apps.utils.managers import PublishedManager
from pytils.translit import translify
from sorl.thumbnail import ImageField

class Question(models.Model):
    pub_date = models.DateTimeField(verbose_name = u'Дата', default=datetime.datetime.now)
    name = models.CharField(max_length = 150, verbose_name = u'Имя', blank = True)
    email = models.CharField(verbose_name=u'E-mail',max_length=75, blank = True)
    question = models.TextField(verbose_name = u'Вопрос')
    answer = models.TextField(verbose_name = u'Ответ', blank = True)
    author = models.CharField(max_length = 150, verbose_name = u'Автор ответа', help_text=u'Например: менеджер',blank=True)
    ans_date = models.DateTimeField(verbose_name = u'Дата ответа', default=datetime.datetime.now, null=True, blank=True)
    send_answer = models.BooleanField(verbose_name = u'отправить ответ на контактный email', default=False)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=False)

    # Managers
    objects = PublishedManager()

    class Meta:
        verbose_name = _(u'question')
        verbose_name_plural = _(u'questions')
        ordering = ['-pub_date']

    def __unicode__(self):
        return u'Вопрос от %s' % self.pub_date

    def get_absolute_url(self):
        return u'/faq/%s/' % self.id

    def save(self, force_insert=False, force_update=False, using=None):
        if self.send_answer:
            subject = u'Ответ на ваш вопрос - %s' % settings.SITE_NAME
            subject = u''.join(subject.splitlines())
            message = render_to_string(
                'faq/user_message_template.html',
                    {
                    'saved_object': self,
                    'site_name': settings.SITE_NAME,
                }
            )
            emailto = self.email
            msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [emailto])
            msg.content_subtype = "html"
            msg.send()
        self.send_answer = False
        if force_insert and force_update:
            raise ValueError("Cannot force both insert and updating in model saving.")
        self.save_base(using=using, force_insert=force_insert, force_update=force_update)

    save.alters_data = True


def file_path_Advice(instance, filename):
    return os.path.join('images','advices',  translify(filename).replace(' ', '_') )

class Advice(models.Model): #консультация визажиста
    pub_date = models.DateTimeField(verbose_name = u'Дата', default=datetime.datetime.now)
    name = models.CharField(max_length = 150, verbose_name = u'Имя')
    email = models.CharField(verbose_name=u'E-mail',max_length=75)
    question = models.TextField(verbose_name = u'Вопрос')
    image = ImageField(verbose_name=u'Изображение', upload_to=file_path_Advice, blank=True)
    answer = models.TextField(verbose_name = u'Ответ', blank = True)
    author = models.CharField(max_length = 150, verbose_name = u'Автор ответа', help_text=u'Например: профессиональный визажист',blank=True)
    ans_date = models.DateTimeField(verbose_name = u'Дата ответа', default=datetime.datetime.now, null=True, blank=True)
    send_answer = models.BooleanField(verbose_name = u'отправить ответ на контактный email', default=False)
    is_published = models.BooleanField(verbose_name = u'Опубликовано', default=False)

    # Managers
    objects = PublishedManager()

    class Meta:
        verbose_name = _(u'advice')
        verbose_name_plural = _(u'advices')
        ordering = ['-pub_date']

    def __unicode__(self):
        return u'Вопрос визажистам от %s' % self.pub_date

    def get_absolute_url(self):
        return u'/visage_advices/%s/' % self.id

    def save(self, force_insert=False, force_update=False, using=None):
        if self.send_answer:
            subject = u'Ответ на ваш вопрос визажистам - %s' % settings.SITE_NAME
            subject = u''.join(subject.splitlines())
            message = render_to_string(
                'faq/user_message_template.html',
                    {
                    'saved_object': self,
                    'site_name': settings.SITE_NAME,
                }
            )
            emailto = self.email
            msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [emailto])
            msg.content_subtype = "html"
            msg.send()
        self.send_answer = False
        if force_insert and force_update:
            raise ValueError("Cannot force both insert and updating in model saving.")
        self.save_base(using=using, force_insert=force_insert, force_update=force_update)

    save.alters_data = True
