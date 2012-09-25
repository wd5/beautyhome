# -*- coding: utf-8 -*-
import datetime
import os
from django.core.mail.message import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView,FormView,DetailView, ListView, View
from pytils.translit import translify
from apps.siteblocks.models import Settings

from forms import QuestionForm, AdviceForm
from models import Question, Advice#,QuestionCategory
import settings


class QuestionListView(FormView):
    form_class = QuestionForm
    template_name = 'faq/faq.html'
    success_url = '/visage_advices/?success=True'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            saved_object = form.save()
            subject = u'%s - Новый вопрос' % settings.SITE_NAME
            subject = u''.join(subject.splitlines())
            message = render_to_string(
                'faq/admin_message_template.html',
                    {
                    'saved_object': saved_object,
                    'site_name': settings.SITE_NAME,
                }
            )
            try:
                emailto = Settings.objects.get(name='workemail').value
            except Settings.DoesNotExist:
                emailto = False

            if emailto:
                msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [emailto])
                msg.content_subtype = "html"
                msg.send()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.published()
        return context

questions_list = QuestionListView.as_view()

class ShowQuestion(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'faq/show_question.html'

show_question = ShowQuestion.as_view()

class VisageAdvicesListView(FormView):
    form_class = AdviceForm
    template_name = 'faq/advices.html'
    success_url = '/visage_advices/?success=True'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        #form = self.get_form(form_class)
        form = AdviceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):

        context = super(VisageAdvicesListView, self).get_context_data(**kwargs)
        context['advices'] = Advice.objects.published()
        return context

show_visage_advices = VisageAdvicesListView.as_view()


class ShowAdvice(DetailView):
    model = Advice
    context_object_name = 'advice'
    template_name = 'faq/show_advice.html'

show_advice = ShowAdvice.as_view()