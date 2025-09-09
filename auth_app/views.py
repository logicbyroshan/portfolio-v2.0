from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.views import View


class SignupView(View):
    """Simple signup view with name, email, and password."""
    
    def get(self, request):
        # Store the redirect URL for after signup
        next_url = request.GET.get('next', '/')
        request.session['next_url'] = next_url
        return render(request, 'auth_app/signup.html')
    
    def post(self, request):
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Basic validation
        if not all([name, email, password]):
            messages.error(request, "All fields are required.")
            return render(request, 'auth_app/signup.html')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists.")
            return render(request, 'auth_app/signup.html')
        
        try:
            # Create user
            user = User.objects.create_user(
                username=email,  # Use email as username
                email=email,
                password=password,
                first_name=name
            )
            
            # Log the user in immediately
            login(request, user)
            messages.success(request, f"Welcome {name}! Your account has been created.")
            
            # Redirect to the original page or home
            next_url = request.session.get('next_url', '/')
            if 'next_url' in request.session:
                del request.session['next_url']
            return redirect(next_url)
            
        except Exception as e:
            messages.error(request, "Error creating account. Please try again.")
            return render(request, 'auth_app/signup.html')


class LoginView(View):
    """Simple login view with email and password."""
    
    def get(self, request):
        # Store the redirect URL for after login
        next_url = request.GET.get('next', '/')
        request.session['next_url'] = next_url
        return render(request, 'auth_app/login.html')
    
    def post(self, request):
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Basic validation
        if not all([email, password]):
            messages.error(request, "Both email and password are required.")
            return render(request, 'auth_app/login.html')
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back {user.first_name}!")
            
            # Redirect to the original page or home
            next_url = request.session.get('next_url', '/')
            if 'next_url' in request.session:
                del request.session['next_url']
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'auth_app/login.html')
