from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='loginuser'),  # Custom login URL
    path('register/', views.signup, name='register'),
    path('index/', views.index, name='index'),
    path('add-expense/', views.add_expense, name='add-expense'),
]