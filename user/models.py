import email
from itertools import product
from urllib import request
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify 
from shop.models import *
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    email=models.EmailField(max_length=100,null=True , blank=True)
    phone=models.CharField(null=True ,blank=True, max_length=50)
    country=models.CharField(null=True ,blank=True, max_length=50)
    city=models.CharField(null=True ,blank=True, max_length=50)
    address=models.CharField(null=True ,blank=True, max_length=50)
    image=models.ImageField(upload_to='users',max_length=None)
    slug=models.SlugField(blank=True)

    def save(self,*args ,**kwargs):
        self.slug=slugify(self.user.username)
        super(Profile,self).save(*args ,**kwargs)
    
    def __str__(self):
        return str(self.user)
    

class Favourite(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE,related_name='favourite')

    def __str__(self):
        return str(self.user)
    