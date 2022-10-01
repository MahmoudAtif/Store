from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index'),

    path('products',views.products, name='products'),
    path('product_details/<slug:slug>/',views.product_details , name='product_details'),
    path('product_category/<int:id>/<slug:slug>',views.product_category, name='product_category'),
    path('remove_comment/<slug:slug>/<int:id>',views.remove_comment , name='remove_comment'),

    path('add_to_cart/<int:id>', views.add_to_cart , name='add_to_cart'),
    path('delete_product_Cart/<int:id>',views.delete_product_cart , name='delete_product_cart'),

    path('about',views.about, name='about'),
    path('contact',views.contact, name='contact'),
    path('cart', views.cart, name='cart'),
    
    path('search',views.search, name='search'),




]
