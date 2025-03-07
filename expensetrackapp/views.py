from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Expense, Category, Budget
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime, timedelta
from django.templatetags.static import static
from django.core.exceptions import ValidationError


def calculate_expense(request):
    """
    Calculate and display the total expense for the current month.
    """
    # Get the current month and year
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    # Calculate the total expense for the logged-in user for the current month
    total_expense = Expense.objects.filter(
        user=request.user,
        date__month=current_month,  # Filter by current month
        date__year=current_year,    # Filter by current year
    ).aggregate(total=Sum('amount'))['total']

    # If no expense exists for the current month, set total_expense to 0
    total_expense = total_expense if total_expense else 0
    return total_expense

    # Pass the total expense to the template


# Helper function to fetch categories for the logged-in user
def get_user_categories():
    """Fetch categories for the logged-in user."""
    return Category.objects.all()

# Create your views here.
@login_required
def index(request):
    """
    Render the index/home page.
    """
    budget = Budget.objects.filter(user=request.user) 
    expense_list = list(Expense.objects.filter(user=request.user).values_list("amount"))
    budget_list = list(Budget.objects.filter(user=request.user).values_list("limit_amount"))
    expense_plain_list = [float(value[0]) for value in expense_list]  # Convert Decimal to float
    budget_plain_list = [float(value[0]) for value in budget_list]  # Convert Decimal to float
    recent_expenses = Expense.objects.all().order_by('-created_at')[:5]
    monthly_expense = calculate_expense(request)
    print(recent_expenses)
    expense_date_list = list(Expense.objects.filter(user=request.user).values_list("date"))
    budget_date_list = list(Budget.objects.filter(user=request.user).values_list("created_at"))

    print(expense_date_list)
    expense_date_plain_list = [str(d[0]) for d in expense_date_list]

    print(expense_date_plain_list)



    expense = Expense.objects.filter(user=request.user)
    # print("budget", budget)
    # print("expense",expense_list)



    return render(request, 'index.html', {
        "expense_plain_list": expense_plain_list,
        "budget_plain_list": budget_plain_list,
         "recent_expenses": recent_expenses,
         "monthly_expense": monthly_expense,
         "expense_date_plain_list": expense_date_plain_list
         })

def logout(request):
    """
    Handle user logout.
    """
    auth_logout(request)  # Use Django's logout function
    messages.success(request, "You have been logged out successfully.")
    return redirect('loginuser')

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
            auth_login(request, user)  # Re-login the user after password change
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
    categories = get_user_categories()  # Fetch categories for the logged-in user
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
    categories = get_user_categories()  # Fetch categories for the logged-in user
    return render(request, 'add-budget.html', {'categories': categories})


@login_required
def download_pdf_report(request):
    # Fetch data for the current month
    today = datetime.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    logo_url = request.build_absolute_uri(static('assets/img/logo.png'))

    # Use `created_at` for filtering
    budgets = Budget.objects.filter(created_at__range=[start_of_month, end_of_month], user=request.user)
    expenses = Expense.objects.filter(created_at__range=[start_of_month, end_of_month], user=request.user)

    # Calculate totals for the summary
    total_budget = sum(budget.limit_amount for budget in budgets)
    total_expenses = sum(expense.amount for expense in expenses)
    remaining_budget = total_budget - total_expenses

    # Render HTML template
    template = get_template('pdf-report.html')
    context = {
        'budgets': budgets,
        'expenses': expenses,
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
        'total_budget': total_budget,
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget,
        'user': request.user,  # Pass the logged-in user
        'app_name': 'Expense Tracker',  # App name
        'logo_url': 'https://example.com/logo.png',  # Replace with your logo URL
    }
    html = template.render(context)

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="monthly_report.pdf"'
    pdf = pisa.CreatePDF(html, dest=response)
    if pdf.err:
        return HttpResponse('Error generating PDF', status=500)
    return response

@login_required
def budget_view(request):
    """
    Calculate and display the total budget for the current month.
    """
    # Get the current month and year
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    # Calculate the total budget for the logged-in user for the current month
    total_budget = Budget.objects.filter(
        user=request.user,
        created_at__month=current_month,  # Filter by current month
        created_at__year=current_year,    # Filter by current year
    ).aggregate(total=Sum('limit_amount'))['total']

    # If no budget exists for the current month, set total_budget to 0
    total_budget = total_budget if total_budget else 0

    # Pass the total budget to the template
    return render(request, 'index.html', {'total_budget': total_budget})


@login_required
def expense_management(request):
    """
    Handle expense management (view, update, delete).
    """
    expenses = Expense.objects.filter(user=request.user)  # Fetch expenses for the logged-in user
    categories = get_user_categories()  # Fetch categories for dropdown

     # Get filter parameters from the request
    category_filter = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Apply filters
    if category_filter:
        expenses = expenses.filter(category_id=category_filter)

    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])

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
    categories = get_user_categories()  # Fetch categories for dropdown

     # Get filter parameter from the request
    category_filter = request.GET.get('category')

    # Apply filter
    if category_filter:
        budgets = budgets.filter(category_id=category_filter)

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