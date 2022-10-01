from django.urls import path

from . import views

urlpatterns = [
    path('checkout',views.checkout, name='checkout'),
    path('delete_order/<slug:code>',views.delete_order, name='delete_order'),

    
]
