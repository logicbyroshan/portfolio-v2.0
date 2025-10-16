from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from portfolio.models import Project, ContactSubmission
from blog.models import Blog, Comment

def admin_dashboard_context(request):
    """Provide statistics for the admin dashboard"""
    if request.path.startswith('/admin/') and request.user.is_staff:
        return {
            'total_projects': Project.objects.count(),
            'total_blogs': Blog.objects.count(), 
            'total_comments': Comment.objects.count(),
            'total_contacts': ContactSubmission.objects.count(),
        }
    return {}