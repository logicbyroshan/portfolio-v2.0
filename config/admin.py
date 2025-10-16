from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

# =========================================================================
# CUSTOM ADMIN SITE
# =========================================================================


class PortfolioAdminSite(admin.AdminSite):
    """Custom admin site with enhanced branding and styling"""

    site_header = "Portfolio Admin Dashboard"
    site_title = "Portfolio Admin"
    index_title = "Welcome to Portfolio Management System"
    site_url = "/"

    def each_context(self, request):
        """Add custom context to all admin pages"""
        context = super().each_context(request)
        context.update(
            {
                "site_header": self.site_header,
                "has_permission": request.user.is_active and request.user.is_staff,
            }
        )
        return context


# Create custom admin site instance
admin_site = PortfolioAdminSite(name="portfolio_admin")

# Register Django's default User and Group models with our custom site
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
