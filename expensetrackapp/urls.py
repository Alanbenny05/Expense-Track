from django.urls import path
from . import views
from django.contrib import admin
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('', views.index,name='index'),
   
    path('', lambda request: redirect('login/'), name='home'),  # Redirect to login page automatically
    path('login/', auth_views.LoginView.as_view(template_name='pages-login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
     path('', views.first, name='first'),
    path('login/', views.pages_login, name='login'),
    path('register/', views.pages_register, name='register'),
]

