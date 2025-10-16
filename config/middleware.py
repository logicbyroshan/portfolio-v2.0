"""
Custom middleware for handling admin and URL-related issues
"""
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)


class AdminURLFixMiddleware(MiddlewareMixin):
    """
    Middleware to handle common admin URL issues and provide better error handling
    """
    
    def process_request(self, request):
        """Process the request and fix common URL issues"""
        path = request.path
        
        # Handle admin URL without trailing slash
        if path == "/admin" and not path.endswith("/"):
            return HttpResponseRedirect("/admin/")
        
        return None
    
    def process_exception(self, request, exception):
        """Log exceptions for debugging"""
        if request.path.startswith("/admin/"):
            logger.error(f"Admin error on {request.path}: {exception}")
        return None