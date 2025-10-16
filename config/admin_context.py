from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


def admin_dashboard_context(request):
    """Provide statistics for the admin dashboard"""
    try:
        if request.path.startswith("/admin/") and request.user.is_authenticated and request.user.is_staff:
            # Import models only when needed to avoid circular imports
            from portfolio.models import Project, ContactSubmission
            from blog.models import Blog, Comment
            
            return {
                "total_projects": Project.objects.count(),
                "total_blogs": Blog.objects.count(),
                "total_comments": Comment.objects.count(),
                "total_contacts": ContactSubmission.objects.count(),
            }
    except Exception as e:
        # Log the error but don't break the request
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Admin context processor error: {e}")
    
    return {}
