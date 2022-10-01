from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import is_valid_path
from shop.models import *
from user.models import *
from .forms import *
from django.utils.crypto import get_random_string
from .models import*
# Create your views here.



def checkout(request):
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
        
        profile=Profile.objects.get(user=request.user)

    else:
        carts=None
        profile=None
        total=0
        total_quantity=0 


    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user=request.user
            data.name=form.cleaned_data['name']
            data.address=form.cleaned_data['address']
            data.city=form.cleaned_data['city']
            data.country=form.cleaned_data['country']
            data.phone=form.cleaned_data['phone']
            data.total=total
            data.code=get_random_string(5).upper()
            data.save()
            for cart in carts:
                data2=OrderProduct()
                data2.order=data
                data2.user=request.user
                data2.product=cart.product
                data2.quantity=cart.quantity
                if cart.variant:
                    data2.variant=cart.variant
                if cart.product.discount:
                    data2.price=cart.get_discount_price
                else:
                    data2.price=cart.get_price
                cart.status='orderd'
                cart.save()
                data2.save()                   
            return redirect('checkout')
        else:
            messages.warning(request , form.error)    
    else:
        form=OrderForm()

    context={
        'carts':carts,
        'total':total,
        'total_quantity':total_quantity,
        'profile':profile,
    }
    return render(request , 'checkout.html',context)




def delete_order(request, code):
    order=Order.objects.get(code=code)
    order.delete()
    return redirect(request.META['HTTP_REFERER'])