from .models import SiteConfiguration, Resume, VideoResume

def site_context(request):
    """
    Context processor to make site configuration available to all templates.
    This ensures footer social links and other global data work across all pages.
    """
    context = {}
    
    # Site Configuration
    try:
        context['config'] = SiteConfiguration.objects.get()
    except SiteConfiguration.DoesNotExist:
        context['config'] = None
        
    # Resume
    try:
        context['resume'] = Resume.objects.get()
    except Resume.DoesNotExist:
        context['resume'] = None
        
    # Video Resume
    try:
        context['video_resume'] = VideoResume.objects.get()
    except VideoResume.DoesNotExist:
        context['video_resume'] = None
    
    return context
