from dataclasses import fields
from django import forms
from .models import *




class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['name','address' , 'city' , 'country' , 'phone']