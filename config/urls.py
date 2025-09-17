from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from music.views import admin_spotify_callback
from portfolio.sitemaps import StaticViewSitemap, BlogSitemap, ProjectSitemap

# Sitemap configuration
sitemaps = {
    'static': StaticViewSitemap,
    'blogs': BlogSitemap,
    'projects': ProjectSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
    path('ai/', include('ai.urls')),
    path('auth/', include('auth_app.urls')),
    path('music/', include('music.urls')),
    path('callback/', admin_spotify_callback, name='spotify_callback'),  # Admin callback for Spotify app config
    
    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
