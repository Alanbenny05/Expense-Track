from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.login_user, name='loginuser'),  # Custom login view
    path('register/', views.signup, name='register'),  # User registration
    path('logout/', views.logout, name='logout'),  # Logout view

    # Dashboard and Core Functionality URLs
    path('index/', views.index, name='index'),  # Home/Dashboard

    # Expense Management URLs
    path('add-expense/', views.add_expense, name='add-expense'),  # Add Expense
    path('expense-management/', views.expense_management, name='expense-management'),  # Expense Management

    # Budget Management URLs
    path('add-budget/', views.add_budget, name='add-budget'),  # Add Budget
    path('budget-management/', views.budget_management, name='budget-management'),  # Budget Management

    # User Profile and Settings URLs
    path('user_profile/', views.user_profile, name='user_profile'),  # User Profile
    path('update_profile/', views.update_profile, name='update_profile'),  # Update Profile
    path('change-password/', views.change_password, name='change_password'),  # Change Password
]