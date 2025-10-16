from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


class CustomAdminSite(AdminSite):
    """Custom admin site with enhanced error handling"""
    
    site_header = _('Portfolio Admin')
    site_title = _('Portfolio Admin')
    index_title = _('Welcome to Portfolio Administration')
    
    def app_index(self, request, app_label, extra_context=None):
        """Override app index with better error handling"""
        try:
            return super().app_index(request, app_label, extra_context)
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Error loading app {app_label}: {str(e)}")
            return self.index(request, extra_context)


# Replace the default admin site
admin.site = CustomAdminSite()
admin.sites.site = admin.site