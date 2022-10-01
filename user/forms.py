from dataclasses import fields
from logging import PlaceHolder
from .models import *
from django.contrib.auth.forms import UserCreationForm  
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  


class CreateUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'username'
    }))

    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Password'
    }))

    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Confirm Password'
    }))

    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Email'
    }))
    class Meta:
        model=User
        fields=['username' , 'password1' , 'password2' , 'email']



class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['phone' , 'address' ,'city' , 'country','image']
        widgets={
            'phone':forms.TextInput(attrs={
                'class':'form-control',
                'Placeholder':'Phone'
            }),
            'address':forms.TextInput(attrs={
                'class':'form-control',
                'Placeholder':'Address'
            }),
            'city':forms.TextInput(attrs={
                'class':'form-control',
                'Placeholder':'City'
            }),
            'country':forms.TextInput(attrs={
                'class':'form-control',
                'Placeholder':'Country'
            }),
            'image':forms.FileInput(attrs={
                'class':'form-control',
                'Placeholder':'Image'
            }),
        }





# class CreateUserForm(UserCreationForm):
#     username=forms.CharField(max_length='50')
#     email = forms.EmailField(label='email')  
#     password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
#     password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  

#     def username_clean(self):
#         username=self.cleaned_data['username'].lower()
#         new=User.objects.filter(username=username)
#         if new:
#             raise ValidationError("User Already Exist")  
#         return username

#     def email_clean(self):
#         email=self.cleaned_data['email']
#         new=User.objects.filter(email=email)
#         if new:
#             raise ValidationError('Email Already Exist')
#         return
    
#     def clean_password2(self):
#         password1=self.cleaned_data['password1']
#         password2=self.cleaned_data['password2']

#         if password1 and password2 and password1!=password2:
#            raise ValidationError("Password don't match") 
        
#         return password2


    
#     def save(self , commit=True):
#         user=User.objects.create_user(
#             self.cleaned_data['username'],  
#             self.cleaned_data['email'],  
#             self.cleaned_data['password1']  
#         )
#         return user