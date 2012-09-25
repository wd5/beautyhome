# -*- coding: utf-8 -*-
from django import forms
from apps.faq.models import Question, Advice

class QuestionForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'E-mail'
            }
        ),
        required=True
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Имя'
            }
        ),
        required=True
    )
    question = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder':'Вопрос'
            }
        ),
        required=True
    )

    class Meta:
        model = Question
        fields = ('name', 'email', 'question',)

class AdviceForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'E-mail'
            }
        ),
        required=True
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Имя'
            }
        ),
        required=True
    )
    question = forms.CharField(
        widget=forms.Textarea(
            attrs={
                #'required':'required',
                'placeholder':'Что интересует'
            }
        ),
        required=True
    )

    image = forms.CharField(
        widget=forms.FileInput(
            attrs={
                'style': 'visibility: hidden; position: absolute;',
            }
        ),
        required=False
    )

    class Meta:
        model = Advice
        fields = ('name', 'email','question','image',)