from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Expense, Category, Budget
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your views here.
def index(request):
    """
    Render the index/home page.
    """
    return render(request, 'index.html')

def logout (request):
    logout(request)
    return redirect ("loginuser")

def signup(request):
    """
    Handle user registration.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")  # Added email field
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "pages-register.html")

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "pages-register.html")

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "pages-register.html")

        # Create the user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            auth_login(request, user)  # Log the user in
            messages.success(request, "Account created successfully!")
            return redirect("index")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, "pages-register.html")

    # If GET request, just render the registration page
    return render(request, "pages-register.html")

def login_user(request):
    """
    Handle user login.
    """
    if request.method == 'POST':
        login_input = request.POST.get('username')  # Can be username or email
        password = request.POST.get('password')

        User = get_user_model()  # Get Django's User model

        try:
            # Check if input is an email
            if '@' in login_input:
                user = User.objects.get(email=login_input)
                username = user.username  # Retrieve the actual username
            else:
                username = login_input  # Assume it's a username

            # Authenticate using username
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, "Login successful!")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('loginuser')
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('loginuser')

    return render(request, 'pages-login.html')

@login_required
def user_profile(request):
    """
    Handle user profile updates.
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # Update profile picture
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            messages.success(request, "Profile picture updated successfully!")
            return redirect('user_profile')

        # Update user details
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')

        if username:
            request.user.username = username
        if full_name:
            request.user.first_name, request.user.last_name = full_name.split(' ', 1)
        if email:
            request.user.email = email

        request.user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('user_profile')

    return render(request, 'users-profile.html', {'user': request.user})

@login_required
def update_profile(request):
    """
    Handle updating user profile.
    """
    return redirect('user_profile')

@login_required
def change_password(request):
    """
    Handle changing user password.
    """
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')

        if new_password != renew_password:
            messages.error(request, "New passwords do not match.")
            return redirect('user_profile')

        user = request.user
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully!")
            return redirect('user_profile')
        else:
            messages.error(request, "Current password is incorrect.")
            return redirect('user_profile')

    return redirect('user_profile')

@login_required
def add_expense(request):
    """
    Handle adding a new expense.
    """
    if request.method == 'POST':
        # Handle form submission for adding an expense
        expense_name = request.POST.get('expense_name')
        amount = request.POST.get('amount')
        category_id = request.POST.get('category')  # Get category ID from the form
        date = request.POST.get('date')
        description = request.POST.get('description')

        # Validate required fields
        if not expense_name or not amount or not category_id or not date:
            messages.error(request, "Please fill in all required fields.")
            return redirect('add-expense')

        try:
            category = Category.objects.get(id=category_id)  # Get the category object
        except Category.DoesNotExist:
            messages.error(request, "Invalid category selected.")
            return redirect('add-expense')

        # Save the expense to the database
        try:
            expense = Expense(
                user=request.user,
                expense_name=expense_name,
                amount=amount,
                category=category,
                date=date,
                description=description,
            )
            expense.save()
            messages.success(request, "Expense added successfully!")
            return redirect('expense-management')  # Redirect to expense management page
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add-expense')

    # If GET request, render the add-expense form
    categories = Category.objects.all()  # Fetch categories for the logged-in user
    return render(request, 'add-expense.html', {'categories': categories})

@login_required
def add_budget(request):
    """
    Handle adding a new budget.
    """
    if request.method == 'POST':
        # Handle form submission for adding a budget
        category_id = request.POST.get('category')  # Get category ID from the form
        limit_amount = request.POST.get('limit_amount')

        # Validate required fields
        if not category_id or not limit_amount:
            messages.error(request, "Please fill in all required fields.")
            return redirect('add-budget')

        try:
            category = Category.objects.get(id=category_id)  # Get the category object
        except Category.DoesNotExist:
            messages.error(request, "Invalid category selected.")
            return redirect('add-budget')

        # Save the budget to the database
        try:
            budget = Budget(
                user=request.user,
                category=category,
                limit_amount=limit_amount,
            )
            budget.save()
            messages.success(request, "Budget added successfully!")
            return redirect('budget-management')  # Redirect to budget management page
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add-budget')

    # If GET request, render the add-budget form
    categories = Category.objects.all()  # Fetch categories for the logged-in user
    return render(request, 'add-budget.html', {'categories': categories})

@login_required
def expense_management(request):
    """
    Handle expense management (view, update, delete).
    """
    expenses = Expense.objects.filter(user=request.user)  # Fetch expenses for the logged-in user
    categories = Category.objects.all()  # Fetch categories for dropdown

    if request.method == 'POST':
        # Handle update or delete action
        action = request.POST.get('action')
        expense_id = request.POST.get('expense_id')

        if action == 'update':
            # Update expense
            expense = get_object_or_404(Expense, id=expense_id, user=request.user)
            expense.expense_name = request.POST.get('expense_name')
            expense.amount = request.POST.get('amount')
            expense.category_id = request.POST.get('category')
            expense.date = request.POST.get('date')
            expense.description = request.POST.get('description')
            expense.save()
            messages.success(request, "Expense updated successfully!")
        elif action == 'delete':
            # Delete expense
            expense = get_object_or_404(Expense, id=expense_id, user=request.user)
            expense.delete()
            messages.success(request, "Expense deleted successfully!")

        return redirect('expense-management')

    return render(request, 'expense-management.html', {'expenses': expenses, 'categories': categories})

@login_required
def budget_management(request):
    """
    Handle budget management (view, update, delete).
    """
    budgets = Budget.objects.filter(user=request.user)  # Fetch budgets for the logged-in user
    categories = Category.objects.all()  # Fetch categories for dropdown

    if request.method == 'POST':
        # Handle update or delete action
        action = request.POST.get('action')
        budget_id = request.POST.get('budget_id')

        if action == 'update':
            # Update budget
            budget = get_object_or_404(Budget, id=budget_id, user=request.user)
            budget.category_id = request.POST.get('category')
            budget.limit_amount = request.POST.get('limit_amount')
            budget.save()
            messages.success(request, "Budget updated successfully!")
        elif action == 'delete':
            # Delete budget
            budget = get_object_or_404(Budget, id=budget_id, user=request.user)
            budget.delete()
            messages.success(request, "Budget deleted successfully!")

        return redirect('budget-management')

    return render(request, 'budget-management.html', {'budgets': budgets, 'categories': categories})