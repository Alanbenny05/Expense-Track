from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='loginuser'),  # Custom login URL
    path('register/', views.signup, name='register'),
    path('index/', views.index, name='index'),
    path('add-expense/', views.add_expense, name='add-expense'),
    path('add-budget/', views.add_budget, name='add-budget'),
    path('update-expense/<int:expense_id>/', views.update_expense, name='update-expense'),  # Update Expense
    path('delete-expense/<int:expense_id>/', views.delete_expense, name='delete-expense'),  # Delete Expense
    path('update-budget/<int:budget_id>/', views.update_budget, name='update-budget'),  # Update Budget
    path('delete-budget/<int:budget_id>/', views.delete_budget, name='delete-budget'),  # Delete Budget
]