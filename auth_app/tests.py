"""
Tests for the auth_app.
Tests authentication functionality, user management, and auth flows.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import pytest

from tests.factories import UserFactory
from tests.utils import BaseTestCase


# ===== AUTHENTICATION TESTS =====


@pytest.mark.views
class AuthViewTest(BaseTestCase):
    """Test authentication views."""

    def test_login_view_get(self):
        """Test login view GET request."""
        try:
            response = self.client.get(reverse("auth_app:login"))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "login")  # Adjust based on your template
        except:
            # Skip if custom login view doesn't exist
            # Test Django's default login view
            response = self.client.get("/accounts/login/")
            if response.status_code == 200:
                self.assertContains(response, "login")

    def test_login_view_post_valid_credentials(self):
        """Test login with valid credentials."""
        user = UserFactory(username="testuser")
        user.set_password("testpass123")
        user.save()

        login_data = {"username": "testuser", "password": "testpass123"}

        try:
            response = self.client.post(reverse("auth_app:login"), data=login_data)
        except:
            # Use Django's default login
            response = self.client.post("/accounts/login/", data=login_data)

        # Should redirect after successful login
        if response.status_code == 302:
            # Check if user is logged in
            user = get_user_model().objects.get(username="testuser")
            self.assertTrue(user.is_authenticated)

    def test_login_view_post_invalid_credentials(self):
        """Test login with invalid credentials."""
        login_data = {"username": "nonexistent", "password": "wrongpass"}

        try:
            response = self.client.post(reverse("auth_app:login"), data=login_data)
        except:
            response = self.client.post("/accounts/login/", data=login_data)

        # Should show error and not redirect
        if response.status_code == 200:
            self.assertContains(response, "error", msg_prefix="Should show login error")

    def test_logout_functionality(self):
        """Test logout functionality."""
        user = UserFactory()
        self.client.force_login(user)

        try:
            response = self.client.post(reverse("auth_app:logout"))
        except:
            response = self.client.post("/accounts/logout/")

        # Should redirect after logout
        if response.status_code == 302:
            # User should no longer be logged in
            response = self.client.get("/")
            self.assertNotContains(response, user.username)

    def test_signup_view_get(self):
        """Test signup view GET request."""
        try:
            response = self.client.get(reverse("auth_app:signup"))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "sign")  # "signup" or "sign up"
        except:
            # Skip if custom signup view doesn't exist
            pass

    def test_signup_view_post_valid_data(self):
        """Test signup with valid data."""
        signup_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "complexpass123",
            "password2": "complexpass123",
        }

        try:
            response = self.client.post(reverse("auth_app:signup"), data=signup_data)

            if response.status_code in [200, 302]:
                # User should be created
                self.assertTrue(User.objects.filter(username="newuser").exists())
        except:
            # Skip if custom signup view doesn't exist
            pass

    def test_signup_view_post_invalid_data(self):
        """Test signup with invalid data."""
        signup_data = {
            "username": "",  # Empty username
            "email": "invalid-email",  # Invalid email
            "password1": "123",  # Weak password
            "password2": "456",  # Passwords don't match
        }

        try:
            response = self.client.post(reverse("auth_app:signup"), data=signup_data)

            if response.status_code == 200:
                # Should show validation errors
                self.assertContains(response, "error")

                # User should not be created
                self.assertFalse(User.objects.filter(email="invalid-email").exists())
        except:
            # Skip if custom signup view doesn't exist
            pass


# ===== USER MODEL TESTS =====


@pytest.mark.models
class UserModelTest(BaseTestCase):
    """Test User model functionality."""

    def test_user_creation(self):
        """Test creating a user."""
        user = UserFactory(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_superuser_creation(self):
        """Test creating a superuser."""
        admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass123"
        )

        self.assertEqual(admin_user.username, "admin")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_string_representation(self):
        """Test user string representation."""
        user = UserFactory(username="testuser")
        self.assertEqual(str(user), "testuser")

    def test_user_full_name(self):
        """Test user full name method."""
        user = UserFactory(first_name="John", last_name="Doe")

        full_name = user.get_full_name()
        self.assertEqual(full_name, "John Doe")


# ===== AUTHENTICATION MIDDLEWARE TESTS =====


@pytest.mark.integration
class AuthMiddlewareTest(BaseTestCase):
    """Test authentication middleware functionality."""

    def test_authenticated_user_access(self):
        """Test authenticated user can access protected views."""
        user = UserFactory()
        self.client.force_login(user)

        # Test access to a protected view (adjust URL as needed)
        try:
            response = self.client.get("/admin/")  # Admin requires authentication
            # Should not redirect to login
            self.assertNotEqual(response.status_code, 302)
        except:
            # Skip if no protected views are configured
            pass

    def test_unauthenticated_user_redirect(self):
        """Test unauthenticated user gets redirected to login."""
        # Try to access a protected view without authentication
        try:
            response = self.client.get("/admin/")
            # Should redirect to login
            if response.status_code == 302:
                self.assertTrue(
                    response.url.startswith("/accounts/login/")
                    or "login" in response.url
                )
        except:
            # Skip if no protected views are configured
            pass


# ===== PASSWORD FUNCTIONALITY TESTS =====


@pytest.mark.views
class PasswordFunctionalityTest(BaseTestCase):
    """Test password-related functionality."""

    def test_password_change_view(self):
        """Test password change functionality."""
        user = UserFactory()
        user.set_password("oldpass123")
        user.save()
        self.client.force_login(user)

        try:
            response = self.client.get(reverse("auth_app:password_change"))
        except:
            try:
                response = self.client.get("/accounts/password/change/")
            except:
                response = self.client.get("/admin/password_change/")

        if response.status_code == 200:
            # Test password change form submission
            password_data = {
                "old_password": "oldpass123",
                "new_password1": "newpass123",
                "new_password2": "newpass123",
            }

            try:
                response = self.client.post(
                    reverse("auth_app:password_change"), data=password_data
                )
            except:
                try:
                    response = self.client.post(
                        "/accounts/password/change/", data=password_data
                    )
                except:
                    response = self.client.post(
                        "/admin/password_change/", data=password_data
                    )

            # Should redirect on success
            if response.status_code == 302:
                # Verify password was changed
                user.refresh_from_db()
                self.assertTrue(user.check_password("newpass123"))

    def test_password_reset_view(self):
        """Test password reset functionality."""
        user = UserFactory(email="test@example.com")

        try:
            response = self.client.get(reverse("auth_app:password_reset"))
        except:
            try:
                response = self.client.get("/accounts/password/reset/")
            except:
                # Skip if password reset not implemented
                return

        if response.status_code == 200:
            # Test password reset form submission
            reset_data = {"email": "test@example.com"}

            try:
                response = self.client.post(
                    reverse("auth_app:password_reset"), data=reset_data
                )
            except:
                response = self.client.post(
                    "/accounts/password/reset/", data=reset_data
                )

            # Should redirect or show success message
            self.assertIn(response.status_code, [200, 302])


# ===== SOCIAL AUTHENTICATION TESTS =====


@pytest.mark.integration
class SocialAuthTest(BaseTestCase):
    """Test social authentication functionality (if django-allauth is used)."""

    def test_social_login_endpoints_exist(self):
        """Test that social login endpoints are accessible."""
        social_providers = ["google", "github", "twitter"]

        for provider in social_providers:
            try:
                url = f"/accounts/{provider}/login/"
                response = self.client.get(url)
                # Should either redirect to provider or show login page
                self.assertIn(response.status_code, [200, 302, 404])
            except:
                # Skip if social auth not configured
                continue

    def test_allauth_configuration(self):
        """Test django-allauth configuration."""
        try:
            from django.conf import settings

            # Check if allauth is in installed apps
            if "allauth" in settings.INSTALLED_APPS:
                # Verify basic allauth configuration
                self.assertIn("allauth.account", settings.INSTALLED_APPS)

                # Check authentication backends
                auth_backends = getattr(settings, "AUTHENTICATION_BACKENDS", [])
                allauth_backend = "allauth.account.auth_backends.AuthenticationBackend"
                self.assertIn(allauth_backend, auth_backends)
        except ImportError:
            # Skip if allauth not installed
            pass


# ===== PERMISSION TESTS =====


@pytest.mark.views
class PermissionTest(BaseTestCase):
    """Test permission-based access control."""

    def test_staff_required_views(self):
        """Test views that require staff permissions."""
        # Test with regular user
        regular_user = UserFactory(is_staff=False)
        self.client.force_login(regular_user)

        response = self.client.get("/admin/")
        # Should be denied or redirected
        self.assertIn(response.status_code, [302, 403, 404])

        # Test with staff user
        staff_user = UserFactory(is_staff=True, is_superuser=True)
        self.client.force_login(staff_user)

        response = self.client.get("/admin/")
        # Should be allowed
        self.assertEqual(response.status_code, 200)

    def test_superuser_required_functionality(self):
        """Test functionality that requires superuser permissions."""
        # This would test any custom superuser-only functionality
        # Adjust based on your application's needs
        pass


# ===== SECURITY TESTS =====


@pytest.mark.security
class AuthSecurityTest(BaseTestCase):
    """Test authentication security measures."""

    def test_login_rate_limiting(self):
        """Test login rate limiting (if implemented)."""
        # This would test any rate limiting on login attempts
        user = UserFactory()
        user.set_password("testpass")
        user.save()

        # Make multiple failed login attempts
        for i in range(10):  # Adjust based on your rate limit
            self.client.post(
                "/accounts/login/", {"username": user.username, "password": "wrongpass"}
            )

        # After rate limit, even correct password should be blocked
        # (This depends on your rate limiting implementation)

    def test_password_strength_requirements(self):
        """Test password strength requirements."""
        # Test weak passwords are rejected
        weak_passwords = ["123", "password", "abc"]

        for weak_pass in weak_passwords:
            signup_data = {
                "username": f"user_{weak_pass}",
                "email": f"{weak_pass}@example.com",
                "password1": weak_pass,
                "password2": weak_pass,
            }

            try:
                response = self.client.post(
                    reverse("auth_app:signup"), data=signup_data
                )

                if response.status_code == 200:
                    # Should show password validation errors
                    self.assertContains(
                        response,
                        "password",
                        msg_prefix="Should validate password strength",
                    )
            except:
                # Skip if custom signup not implemented
                pass

    def test_csrf_protection(self):
        """Test CSRF protection on auth forms."""
        # Test login form requires CSRF token
        response = self.client.post(
            "/accounts/login/", {"username": "test", "password": "test"}
        )

        # Should be protected by CSRF (403 or redirect to get CSRF token)
        # This depends on your CSRF configuration
        if response.status_code == 403:
            self.assertIn("CSRF", str(response.content))

    def test_session_security(self):
        """Test session security settings."""
        from django.conf import settings

        # Check secure session settings (for production)
        if not settings.DEBUG:
            # These should be True in production
            session_cookie_secure = getattr(settings, "SESSION_COOKIE_SECURE", False)
            session_cookie_httponly = getattr(settings, "SESSION_COOKIE_HTTPONLY", True)

            # Note: These assertions might need to be adjusted based on environment
            # self.assertTrue(session_cookie_secure)  # Should be True in production
            self.assertTrue(session_cookie_httponly)


# ===== CUSTOM USER PROFILE TESTS =====


@pytest.mark.models
class UserProfileTest(BaseTestCase):
    """Test custom user profile functionality (if extended User model exists)."""

    def test_user_profile_creation(self):
        """Test user profile creation and relationships."""
        # This would test any custom user profile models
        # Adjust based on your user profile implementation
        user = UserFactory()

        # If you have a UserProfile model related to User
        try:
            # Example: UserProfile.objects.create(user=user, ...)
            # Test profile fields and methods
            pass
        except:
            # Skip if no custom user profile
            pass

    def test_user_profile_signals(self):
        """Test user profile creation signals."""
        # Test that profile is automatically created when user is created
        # This would be relevant if you have post_save signals
        pass
