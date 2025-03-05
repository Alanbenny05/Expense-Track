from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_user, name='loginuser'),  # Custom login URL
    path('register/', views.signup, name='register'),
    path('', views.index, name='index'),
    path('add-expense/', views.add_expense, name='add-expense'),  # Add Expense
    path('add-budget/', views.add_budget, name='add-budget'),  # Add Budget
    path('budget-management/', views.budget_management, name='budget-management'),  # Budget Management
    path('expense-management/', views.expense_management, name='expense-management'),  # Expense Management
    path('user_profile/', views.user_profile, name='user_profile'),  # User Profile
    path('update-profile/', views.update_profile, name='update_profile'),  # Update Profile
    path('change-password/', views.change_password, name='change_password'),  # Change Password
    path('logout/', views.logout, name='logout'),  # Logout URL
]