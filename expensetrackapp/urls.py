from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import download_pdf_report
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.login_user, name='loginuser'),  # Custom login view
    path('register/', views.signup, name='register'),  # User registration
    path('logout/', views.logout, name='logout'),  # Logout view
    path('index/', views.index, name='index'),  # Home/Dashboard
    path('add-expense/', views.add_expense, name='add-expense'),  # Add Expense
    path('expense_management/', views.expense_management, name='expense-management'),  # Expense Management
    path('add-budget/', views.add_budget, name='add-budget'),  # Add Budget
    path('budget-management/', views.budget_management, name='budget-management'),  # Budget Management
    path('user_profile/', views.user_profile, name='user_profile'),  # User Profile
    path('update_profile/', views.update_profile, name='update_profile'),  # Update Profile
    path('change-password/', views.change_password, name='change_password'),  # Change Password
    path('download-pdf-report/', download_pdf_report, name='download_pdf_report'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)