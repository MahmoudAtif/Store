from dataclasses import fields
from pyexpat import model
from .models import *

from django import forms 


class ContactForm(forms.ModelForm):
    class Meta:
        model=ContactMessage
        fields=['name','email','subject','message']
        widgets={
            'name':forms.TextInput(attrs={
                'placeholder':'Name',
                'class':'form-control'
            }),
             'email':forms.EmailInput(attrs={
                'placeholder':'email',
                'class':'form-control'
            }),
             'subject':forms.TextInput(attrs={
                'placeholder':'subject',
                'class':'form-control'
            }),
             'message':forms.Textarea(attrs={
                'placeholder':'message',
                'class':'form-control'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment','rate']



class ShopCartForm(forms.ModelForm):
    
    class Meta:
        model = ShopCart
        fields = ['quantity']
