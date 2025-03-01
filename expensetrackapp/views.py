from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
# Rename to avoid conflict
from .models import UserProfile  
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")  # Ensure password is assigned here
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "pages-register.html", {"error": "Passwords do not match"})

        user = User.objects.create_user(username=username, password=password)
        user.save()

        login(request, user)
        return redirect("dashboard")

    # If GET request, just render the registration page
    return render(request, "pages-register.html")

# login_user
def login_user(request):
    if request.method == 'POST':
        login_input = request.POST.get('username')  # Can be username or email
        password = request.POST.get('password')

        User = get_user_model()  # Get Django's User model

        try:
            # Check if input is an email
            user = User.objects.get(email=login_input)
            username = user.username  # Retrieve the actual username
        except User.DoesNotExist:
            username = login_input  # Assume it's a username

        # Authenticate using username
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('index')  
        else:
            messages.error(request, "Invalid email or password")
            return redirect('loginuser')

    return render(request, 'pages-login.html')

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')

    else:
        form = UserProfile(instance=profile)

    return render(request, 'expensetrackapp/users-profile.html', {'forms': form})








