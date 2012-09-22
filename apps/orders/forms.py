# -*- coding: utf-8 -*-
from django import forms
from apps.orders.models import Order

class RegistrationOrderForm(forms.ModelForm):
    first_name = forms.CharField(error_messages={'required': 'Введите ваше имя'}, widget=forms.TextInput(attrs={'class':'input1'}))
    last_name = forms.CharField(error_messages={'required': 'Введите вашу фамилию'}, widget=forms.TextInput(attrs={'class':'input1'}))
    email = forms.EmailField(error_messages={'required': 'Введите ваш e-mail'}, widget=forms.TextInput(attrs={'class':'input1'}))
    phone = forms.CharField(error_messages={'required': 'Введите ваш номер телефона'}, widget=forms.TextInput(attrs={'class':'input1'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'input2'}), required=False)
    note = forms.CharField(
        widget=forms.Textarea(attrs={'class':'textarea1'}),
        required=False
    )

    class Meta:
        model = Order
        exclude = ('create_date',)

    def clean(self):
        cleaned_data = super(RegistrationOrderForm, self).clean()
        order_carting = cleaned_data.get("order_carting")
        address = cleaned_data.get("address")

        if order_carting == 'carting' and address=='':
            raise forms.ValidationError("Введите адрес доставки")

        return cleaned_data