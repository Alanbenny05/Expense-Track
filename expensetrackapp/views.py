from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Expense, Category, Budget  # Import Budget model
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
        form = UserProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('user_profile')
        else:
            messages.error(request, "Invalid form data. Please check your inputs.")
    else:
        form = UserProfile(instance=profile)

    return render(request, 'expensetrackapp/users-profile.html', {'forms': form})

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
        payment_method = request.POST.get('payment_method')
        description = request.POST.get('description')
        print("expense name:", expense_name)
        print("amount:", amount)
        print("category_id:", category_id)
        print("date:", date)

        # Validate required fields
        if not expense_name or not amount or not category_id or not date:
            messages.error(request, "Please fill in all required fields.")
            print("inside if")
            return redirect('add-expense')

        try:
            category = Category.objects.get(id=category_id)  # Get the category object
        except Category.DoesNotExist:
            messages.error(request, "Invalid category selected.")
            print("inside invalid category")
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
            print(expense)
            messages.success(request, "Expense added successfully!")
            return redirect('index')  # Redirect to the index page after adding the expense
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            print(e)
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
            return redirect('index')  # Redirect to the index page after adding the budget
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('add-budget')

    # If GET request, render the add-budget form
    categories = Category.objects.all()  # Fetch categories for the logged-in user
    return render(request, 'add-budget.html', {'categories': categories})

@login_required
def update_expense(request, expense_id):
    """
    Handle updating an existing expense.
    """
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)  # Ensure the expense belongs to the user
    if request.method == 'POST':
        # Update the expense with the new data
        expense.expense_name = request.POST.get('expense_name')
        expense.amount = request.POST.get('amount')
        expense.category_id = request.POST.get('category')
        expense.date = request.POST.get('date')
        expense.description = request.POST.get('description')
        expense.save()
        messages.success(request, "Expense updated successfully!")
        return redirect('index')
    else:
        # Render the update form with the current expense data
        categories = Category.objects.all()
        return render(request, 'update-expense.html', {'expense': expense, 'categories': categories})

@login_required
def delete_expense(request, expense_id):
    """
    Handle deleting an existing expense.
    """
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)  # Ensure the expense belongs to the user
    expense.delete()
    messages.success(request, "Expense deleted successfully!")
    return redirect('index')

@login_required
def update_budget(request, budget_id):
    """
    Handle updating an existing budget.
    """
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)  # Ensure the budget belongs to the user
    if request.method == 'POST':
        # Update the budget with the new data
        budget.category_id = request.POST.get('category')
        budget.limit_amount = request.POST.get('limit_amount')
        budget.save()
        messages.success(request, "Budget updated successfully!")
        return redirect('index')
    else:
        # Render the update form with the current budget data
        categories = Category.objects.all()
        return render(request, 'update-budget.html', {'budget': budget, 'categories': categories})

@login_required
def delete_budget(request, budget_id):
    """
    Handle deleting an existing budget.
    """
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)  # Ensure the budget belongs to the user
    budget.delete()
    messages.success(request, "Budget deleted successfully!")
    return redirect('index')