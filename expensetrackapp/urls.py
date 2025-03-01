from django.urls import path
from . import views

from django.shortcuts import redirect
from django.contrib.auth import views as auth_views


urlpatterns=[
    
    path('login/', views.login_user, name='loginuser'), 
    path('register/', views.signup, name='register'),
    path('index/', views.index,name='index'),
]