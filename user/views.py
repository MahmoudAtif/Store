from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import logout ,authenticate , login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import *
from .decorators import *
from .models import *
from order.models import *
from shop.filters import *
# Create your views here.

@authenticated_user
def register_page(request):
    if request.method=='POST':
        form= CreateUserForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            new=User.objects.filter(email=email)
            if new:
                messages.warning(request , 'email already exist')
            else:
                form.save()
            return redirect('register_page')
    else:
        form= CreateUserForm()


    context={
        'form':form
    }
    return render(request , 'register.html',context)

@authenticated_user
def login_page(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request , username=username , password=password)
        if user is not None:
            login(request , user)
            return redirect('index')
        else:
            messages.warning(request,'username or password is incorrect')
    return render(request , 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login_page')


@login_required(login_url='login_page')
def myAccount(request):
    profile=Profile.objects.get(user=request.user)
    context={
        'profile':profile,
    }
    return render(request, 'user_profile.html',context)




@login_required(login_url='login_page')
def update_myAccount(request):
    profile=Profile.objects.get(user=request.user)
    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request , 'Profile updated successfully')
            return redirect('myaccount')
        else:
            messages.warning(request,form.error)
    else:    
        form=ProfileForm(instance=profile)
    
    
    context={
        'profile':profile,
        'form':form,
    }
    return render(request, 'user_update.html',context)


@login_required(login_url='login_page')
def myorders(request):
    if request.method=='GET':
        status=request.GET.get('status')
        if status:
            orders=Order.objects.filter(user=request.user , status=status)
        else:
            orders=Order.objects.filter(user=request.user).order_by('-date_created')

    context={
        'orders':orders,
    }
    return render(request , 'user_orders.html',context)


@login_required(login_url='login_page')
def myOrder_detail(request,code):
    order=Order.objects.get(code=code )
 
    context={
        'order':order,
    }
    return render(request , 'user_order_detail.html',context)


@login_required(login_url='login_page')
def favourite(request):
    products=Product.objects.filter(wishlist=request.user)

    context={
        'products':products,
    }
    return render(request, 'favourite.html',context)


@login_required(login_url='login_page')
def add_to_favourite(request , id):
    product=Product.objects.get(id=id)
    if not request.user in product.wishlist.all():
        product.wishlist.add(request.user)       
    else:
        product.wishlist.remove(request.user)

    return redirect(request.META['HTTP_REFERER'])



@login_required(login_url='login_page')
def comments(request):
    comments=Comment.objects.filter(user=request.user)
    categorys=Category.objects.all()
    products=Product.objects.filter(status=True)

    context={
        'comments':comments,
        'categorys':categorys,
        'products':products,
    }
    return render(request , 'user_comments.html',context)


def change_password(request):

    if request.method=='POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            messages.success(request , 'Password Change Successfully')
        else:
            messages.warning(request , str(form.errors))                
    else:
        form = PasswordChangeForm(request.user)
    
    context={
        'form':form,
    }

    return render(request , 'change_password.html',context)