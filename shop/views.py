from multiprocessing import context
from unicodedata import category
from urllib import request
from django.shortcuts import render , redirect

from user.models import Favourite
from .forms import *
from .models import *
from django.contrib import messages
from.filters import *
from django.contrib.auth import logout 
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
# Create your views here.


def index(request):
    # categorys=Category.objects.all()
    products=Product.objects.filter(status=True)
    latest_products=products.order_by('-id')

    ############### Cart ####################
    if request.user.is_authenticated:
        carts=ShopCart.objects.filter(user=request.user,status='pending')
        total=0
        total_quantity=0   
        for item in carts:
            # total_quantity+=item.quantity
            if item.product.discount:
                total+=item.get_discount_price
            else:
                total+= item.get_price
        
        for item in carts:
            total_quantity+=item.quantity
    else:
        carts=None
        total=0
        total_quantity=0 
    ############### endCart #################
   

    page='home'
    
    context={
        'page':page,
        'products':products,
        'latest_products':latest_products,
        'carts':carts,
        'total':total,
        'total_quantity':total_quantity,
    }
    return render(request, 'index.html',context)


def search(request):
    category=request.GET.get('category')
    product=request.GET.get('product')
    if request.method=='GET':
        if category=='0':
            products=Product.objects.filter(name__contains=product , status=True)    
        elif product == None:
            products=Product.objects.filter(category=category , status=True)
        else:
            products=Product.objects.filter(name__contains=product ,category=category , status=True)
    else:
        products=Product.objects.filter(status=True)

     ############### Cart ####################
    if request.user.is_authenticated:
        carts=ShopCart.objects.filter(user=request.user,status='pending')
        total=0
        total_quantity=0   
        for item in carts:
            # total_quantity+=item.quantity
            if item.product.discount:
                total+=item.get_discount_price
            else:
                total+= item.get_price
        
        for item in carts:
            total_quantity+=item.quantity
    else:
        carts=None
        total=0
        total_quantity=0 
    ############### endCart #################

    context={
        'products':products,
        'carts':carts,
        'total':total,
        'total_quantity':total_quantity,
    }        
    return render(request, 'search.html',context)


def products(request):
    products=Product.objects.filter(status=True)
    ############### Cart ####################
    if request.user.is_authenticated:
        carts=ShopCart.objects.filter(user=request.user,status='pending')
        total=0
        total_quantity=0   
        for item in carts:
            # total_quantity+=item.quantity
            if item.product.discount:
                total+=item.get_discount_price
            else:
                total+= item.get_price
        
        for item in carts:
            total_quantity+=item.quantity
    else:
        carts=None
        total=0
        total_quantity=0 
    colors=Color.objects.all()
    sizes=Size.objects.all()

    ###### Price Filter #########
    if request.method == 'GET':
        ordering=request.GET.get('ordering')
        if ordering:
            products=products.order_by(ordering)
   
    ########## pagination ############
    paginator=Paginator(products , 10)
    page_number=request.GET.get('page')
    objects=paginator.get_page(page_number)

    
    pro='test'  
    context={
        
        'products':objects,
        'carts':carts,
        'total':total,
        'total_quantity':total_quantity,
        'pro':pro,
        'colors':colors,
        'sizes':sizes,
    }
    return render(request, 'products.html',context)





def product_details(request,slug):   
    product=Product.objects.get(slug=slug)
    products=Product.objects.filter(category=product.category,status=True)
    comments=product.comment.all().order_by('-id')
    variant=Variant.objects.filter(product=product)

    if request.user.is_authenticated:
        if request.method=='POST':
            commentForm=CommentForm(request.POST)
            if commentForm.is_valid():
                data=Comment()
                data.product= product
                data.user= request.user
                data.comment= commentForm.cleaned_data['comment']
                data.rate= commentForm.cleaned_data['rate']   
                data.save()
                messages.success(request,'Thanks For Review ')
        else:
            commentForm=CommentForm()      
    
        ####### Cart ######
        carts=ShopCart.objects.filter(user=request.user,status='pending')
        total=0
        total_quantity=0   
        for item in carts:
            if item.product.discount:
                total+=item.get_discount_price
            else:
                total+= item.get_price
        
        for item in carts:
            total_quantity+=item.quantity
    else:
        commentForm=CommentForm() 
        carts=None
        total=0
        total_quantity=0      
        messages.warning(request, 'Login required')
        ####### endCart ######
    
   


    #### pagination #############
    paginator=Paginator(comments , 5)
    page_number=request.GET.get('page')
    page_comments=paginator.get_page(page_number)
    
            
    context={
        'products':products,
        'product':product,
        'commentForm':commentForm,
        'comments':page_comments,
        'carts':carts,
        'total':total,
        'total_quantity':total_quantity,
        'variant':variant
        
    }
    return render(request , 'product_details.html',context)



def about(request):
    setting=Setting.objects.get(pk=1)

    ############### Cart ####################
    if request.user.is_authenticated:
        carts=ShopCart.objects.filter(user=request.user,status='pending')
        total=0
        total_quantity=0   
        for item in carts:
            # total_quantity+=item.quantity
            if item.product.discount:
                total+=item.get_discount_price
            else:
                total+= item.get_price
        
        for item in carts:
            total_quantity+=item.quantity
    else:
        carts=None
        total=0
        total_quantity=0 

    context={
        'setting':setting,
        # 'categorys':categorys,
        'carts':carts,
        'total':total,
        'total_quantity':total_quantity,
    }

    return render(request,'about.html',context)

def contact(request):
    setting=Setting.objects.get(pk=1)
    form=ContactForm()
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your message sent sucessfully')
            return redirect('contact')
    
    ############### Cart ####################
    if request.user.is_authenticated:
        carts=ShopCart.objects.filter(user=request.user,status='pending')
        total=0
        total_quantity=0   
        for item in carts:
            if item.product.discount:
                total+=item.get_discount_price
            else:
                total+= item.get_price
        
        for item in carts:
            total_quantity+=item.quantity
    else:
        carts=None
        total=0
        total_quantity=0 

    context={
        'form':form,
        'setting':setting,
        'carts':carts,
        'total':total,
        'total_quantity':total_quantity,
        
    }
    return render(request,'contactus.html',context)

def product_category(request,id,slug):
    products=Product.objects.filter(category=id,status=True)
    ############### Cart ####################
    if request.user.is_authenticated:
        carts=ShopCart.objects.filter(user=request.user,status='pending')
        total=0
        total_quantity=0   
        for item in carts:
            # total_quantity+=item.quantity
            if item.product.discount:
                total+=item.get_discount_price
            else:
                total+= item.get_price
        
        for item in carts:
            total_quantity+=item.quantity
    else:
        carts=None
        total=0
        total_quantity=0 
    
    if request.method == 'GET':
        ordering=request.GET.get('ordering')
        if ordering:
            products=products.order_by(ordering)
    #### pagination
    paginator=Paginator(products , 10)
    page_number=request.GET.get('page')
    objects=paginator.get_page(page_number)

    context={
        'products':objects,
        'carts':carts,
        'total':total,
        'total_quantity':total_quantity,
    }
    return render(request, 'product_category.html',context)


@login_required(login_url='index')
def remove_comment(request , slug,id):
    product=Product.objects.get(slug=slug)
    comment=product.comment.get(id=id)
    comment.delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='index')
def add_to_cart(request, id):
    product=Product.objects.get(id=id)
    if request.method=='POST':
        form=ShopCartForm(request.POST)
        size_color_id=request.POST["size-color"]
        var=Variant.objects.get(id=size_color_id)
        userProduct=ShopCart.objects.filter(product=product,user=request.user,variant=var,status='pending')
        if form.is_valid():
            if not userProduct:
                data=ShopCart()
                data.user=request.user
                data.product=product
                data.quantity=form.cleaned_data['quantity']
                if product.variant.all:
                    data.variant=var
                if data.quantity >=1:
                    data.save()
                else:
                    messages.warning(request , 'invalid quantity')
                    return redirect(request.META['HTTP_REFERER'])
            else:
                userProduct=ShopCart.objects.get(product=product,user=request.user,variant=var,status='pending')
                userProduct.quantity=form.cleaned_data['quantity']
                if userProduct.quantity >=1:
                    userProduct.save()        
                else:
                    messages.warning(request , 'invalid quantity')
                    return redirect(request.META['HTTP_REFERER'])
        return redirect('cart')
    else:      
        return redirect('/product_details/'+product.slug)
         

def cart(request):
    if request.user.is_authenticated:
        carts=ShopCart.objects.filter(user=request.user,status='pending')
        total=0
        total_quantity=0   

        for item in carts:
            if item.product.discount:
                total+=item.get_discount_price
            else:
                total+= item.get_price
        
        for item in carts:
            total_quantity+=item.quantity
    else:
        carts=None
        total=0
        total_quantity=0 

    
    context={
        'carts':carts,
        'total':total,
        'total_quantity':total_quantity,
    }
    return render(request,'cart.html',context)


def delete_product_cart(request, id):
    product=ShopCart.objects.get(user=request.user , product=id,status='pending')
    product.delete()
    return redirect(request.META['HTTP_REFERER'])






