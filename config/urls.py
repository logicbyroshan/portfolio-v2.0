from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from music.views import spotify_callback

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
    path('ai/', include('ai.urls')),
    path('auth/', include('auth_app.urls')),
    path('music/', include('music.urls')),
    path('callback/', spotify_callback, name='spotify_callback'),  # Direct callback URL to match Spotify app config
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
