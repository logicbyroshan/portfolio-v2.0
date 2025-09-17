from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


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


class ForgotPasswordView(View):
    """Handle forgot password requests."""
    
    def get(self, request):
        return render(request, 'auth_app/forgot_password.html')
    
    def post(self, request):
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, "Email address is required.")
            return render(request, 'auth_app/forgot_password.html')
        
        try:
            user = User.objects.get(email=email)
            
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Get current site
            current_site = get_current_site(request)
            
            # Create reset link
            reset_link = request.build_absolute_uri(
                reverse('auth_app:reset_password', kwargs={'uidb64': uid, 'token': token})
            )
            
            # Prepare email context
            context = {
                'user': user,
                'reset_link': reset_link,
                'site_name': current_site.name,
                'domain': current_site.domain,
            }
            
            # Render email template
            subject = f'Password Reset - {current_site.name}'
            html_message = render_to_string('emails/password_reset.html', context)
            plain_message = render_to_string('emails/password_reset.txt', context)
            
            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
            messages.success(request, 
                "If an account with this email exists, you will receive a password reset link shortly.")
            return redirect('auth_app:login')
            
        except User.DoesNotExist:
            # Don't reveal that the user doesn't exist for security
            messages.success(request, 
                "If an account with this email exists, you will receive a password reset link shortly.")
            return redirect('auth_app:login')
        except Exception as e:
            messages.error(request, "Error sending email. Please try again later.")
            return render(request, 'auth_app/forgot_password.html')


class ResetPasswordView(View):
    """Handle password reset with token verification."""
    
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if default_token_generator.check_token(user, token):
                # Token is valid
                context = {
                    'uidb64': uidb64,
                    'token': token,
                    'user': user,
                }
                return render(request, 'auth_app/reset_password.html', context)
            else:
                messages.error(request, "Invalid or expired reset link.")
                return redirect('auth_app:forgot_password')
                
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Invalid reset link.")
            return redirect('auth_app:forgot_password')
    
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if not default_token_generator.check_token(user, token):
                messages.error(request, "Invalid or expired reset link.")
                return redirect('auth_app:forgot_password')
            
            password = request.POST.get('password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()
            
            # Validation
            if not password:
                messages.error(request, "Password is required.")
                context = {'uidb64': uidb64, 'token': token, 'user': user}
                return render(request, 'auth_app/reset_password.html', context)
            
            if len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
                context = {'uidb64': uidb64, 'token': token, 'user': user}
                return render(request, 'auth_app/reset_password.html', context)
            
            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                context = {'uidb64': uidb64, 'token': token, 'user': user}
                return render(request, 'auth_app/reset_password.html', context)
            
            # Update password
            user.set_password(password)
            user.save()
            
            messages.success(request, "Your password has been reset successfully. You can now sign in.")
            return redirect('auth_app:login')
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, "Invalid reset link.")
            return redirect('auth_app:forgot_password')
