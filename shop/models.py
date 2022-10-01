from audioop import avg
from email.mime import image
from itertools import product
from unicodedata import name
from django.db import models
from django.db.models import Avg ,Count ,Max ,Min
from django.utils.text import slugify
from math import *
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True,max_length=255)
    image=models.ImageField(null=True ,blank=True,upload_to='category_images')
    status=models.BooleanField(default=True)
    slug=models.SlugField(null=True ,blank=True)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=('name','slug')

    def save(self , *args , **kwargs):
        self.slug=slugify(self.name)
        super(Category, self).save(*args , **kwargs)

    def __str__(self):
        return self.name
    

    


class Product(models.Model):
    # VARIANTS = (
    #     ('None', 'None'),
    #     ('Size', 'Size'),
    #     ('Color', 'Color'),
    #     ('Size-Color', 'Size-Color'),

    # )
    category = models.ForeignKey(Category, on_delete=models.CASCADE , related_name='product') #many to one relation with Category
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=255, null=True , blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    amount=models.IntegerField(default=0)
    discount=models.IntegerField()
    brand = models.CharField(max_length=150, null=True , blank=True)
    wishlist=models.ManyToManyField(User , related_name='productFav')
    # minamount=models.IntegerField(default=3)
    # variant=models.CharField(max_length=10,choices=VARIANTS, default='None')
    slug = models.SlugField(null=True , blank=True)
    status=models.BooleanField(default=True)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)
      
    
    class Meta:
        unique_together = ('name','slug')
        ordering=['-price']
    
    @property
    def get_total(self):
        total=self.price-(self.price * self.discount/100)     
        return round(total,2)
    
    @property
    def get_rate(self):
        comments=Comment.objects.filter(product=self).aggregate(average=Avg('rate'))
        average=round(comments['average'])
        return average
    
    @property
    def get_total_rate(self):
        comments=Comment.objects.filter(product=self).aggregate(count=Count('id'))
        count=round(comments['count'])
        return count
    
    @property
    def get_min_price(self):
        products=self.objects.filter(status=True).aggregate(Min=Min('price'))
        min_price=products['min']
        return min_price
    
    @property
    def get_max_price(self):
        products=self.objects.all().aggregate(max=Max('price'))
        max_price=products['max']
        return max_price

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name





class Size(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Color(models.Model):
    name=models.CharField(max_length=50)
    code=models.CharField(max_length=150 , null=True , blank=True)
    def __str__(self):
        return self.name


class Variant(models.Model):
    product=models.ForeignKey(Product,  on_delete=models.CASCADE,related_name='variant')
    size=models.ForeignKey(Size,  on_delete=models.CASCADE)
    color=models.ForeignKey(Color,  on_delete=models.CASCADE)
    image=models.ImageField(upload_to='variant_images' , null=True , blank=True)
    
    def __str__(self):
        return str(self.product)

    





class ProductImages(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE ,related_name='productImage')
    image=models.ImageField(upload_to='product_images/' ,null=True , blank=True)
    def __str__(self):
        return str(self.product)


class ShopCart(models.Model):
    CHOICES=(
        ('pending','pending'),
        ('orderd','orderd')
    )
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE,related_name='productCart')
    quantity=models.IntegerField(default=1, blank=True)
    variant=models.ForeignKey(Variant , on_delete=models.CASCADE, null=True , blank=True)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=50 , choices=CHOICES, default='pending')
    
    @property
    def get_price(self):
        total= self.product.price * self.quantity
        return total

    @property
    def get_discount_price(self):
        total= self.product.get_total * self.quantity
        return total


    def __str__(self):
        return str(self.product)

class Setting(models.Model):
    name = models.CharField(max_length=150)
    keywords = models.CharField(null=True,blank=True,max_length=255)
    description = models.TextField(null=True,max_length=255)
    company = models.CharField(null=True,blank=True,max_length=50)
    address = models.CharField(null=True,blank=True,max_length=100)
    phone = models.CharField(null=True,blank=True,max_length=15)
    fax = models.CharField(null=True,blank=True,max_length=15)
    email = models.CharField(null=True,blank=True,max_length=50)
    smtpserver = models.CharField(null=True,blank=True,max_length=50)
    smtpemail = models.CharField(null=True,blank=True,max_length=50)
    smtppassword = models.CharField(null=True,blank=True,max_length=10)
    smtpport = models.CharField(null=True,blank=True,max_length=5)
    icon = models.ImageField(null=True,blank=True,upload_to='images/')
    facebook = models.CharField(null=True,blank=True,max_length=50)
    instegram = models.CharField(null=True,blank=True,max_length=50)
    twitter = models.CharField(null=True,blank=True,max_length=50)
    youtube = models.CharField(null=True,blank=True, max_length=50)
    status=models.BooleanField(default=True)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name= models.CharField(max_length=20)
    email= models.EmailField(max_length=50)
    subject= models.CharField(max_length=50)
    message= models.TextField(max_length=255)
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE, related_name='comment')
    # subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField()
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return str(self.user)






    