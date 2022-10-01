from django import forms
import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):

    name=forms.CharField(widget=forms.TextInput(attrs={
        'class':'input search-input',
        'placeholder':'Enter your keyword'
    }))

    class Meta:
        model=Product
        fields=['category','name']
