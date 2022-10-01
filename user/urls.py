from django import views
from django.urls import path , include
from . import views
from .api import views as apiViews
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)



router=DefaultRouter()
router.register('users',apiViews.User_list2)
router.register('products',apiViews.ProductList)
router.register('comments',apiViews.CommentList)
router.register('login',apiViews.LoginView)
# router.register('register',apiViews.RegisterView)

urlpatterns = [
    path('user_logout',views.user_logout ,name='user_logout'),
    path('login',views.login_page ,name='login_page'),
    path('register',views.register_page ,name='register_page'),
    path('myaccount',views.myAccount ,name='myaccount'),
    path('updateMyaccount',views.update_myAccount ,name='updateMyaccount'),
   
    path('myorders',views.myorders ,name='myorders'),
    path('myOrderDetail/<slug:code>',views.myOrder_detail ,name='orderdetail'),
   
    path('favourite',views.favourite ,name='favourite'),
    path('add_to_favourite/<int:id>',views.add_to_favourite ,name='add_to_favourite'),
   
    path('comments',views.comments ,name='comments'),
    path('ChangePassword',views.change_password ,name='ChangePassword'),




    path('usersjson/',apiViews.Users_list.as_view() ,name='usersjson'),
    path('usersjson2/',include(router.urls)),
    path('usersjson3/', apiViews.usersjson3 ,name='usersjson3'),
    path('usersjson3/<int:id>/', apiViews.userjson3 ,name='usersjson3'),
    path('findProducts/' , apiViews.find_products , name='find_products'),
    
    # allow logout in API
    path('api-auth' , include('rest_framework.urls')),
    # token
    path('api-auth-token/' , obtain_auth_token),
    
    path('registerApiView/', apiViews.RegisterApiView.as_view(),name='register'),

    #######JWT(JSON WEB TOKEN)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify' , TokenVerifyView.as_view() ,name='token_verify'),



    
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
]
