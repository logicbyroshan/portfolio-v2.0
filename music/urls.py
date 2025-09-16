from django.urls import path
from . import views

urlpatterns = [
    # Public routes
    path("", views.my_playlist, name="my_playlist"),
    path("my-playlist/", views.my_playlist, name="my_playlist"),
    path("playlist/<str:playlist_id>/", views.playlist_detail, name="playlist_detail"),
    path("playlist/<str:playlist_id>/tracks/", views.get_playlist_tracks, name="get_playlist_tracks"),
    
    # Admin routes for Spotify sync
    path("admin/spotify-login/", views.admin_spotify_login, name="admin_spotify_login"),
    path("admin/spotify-callback/", views.admin_spotify_callback, name="admin_spotify_callback"),
    path("admin/spotify-sync/", views.admin_spotify_sync, name="admin_spotify_sync"),
    
    # Legacy routes for backward compatibility
    path("spotify-login/", views.spotify_login, name="spotify_login"),
    path("spotify-callback/", views.spotify_callback, name="spotify_callback"),
    path("playlist/<str:playlist_id>/tracks/", views.playlist_tracks, name="playlist_tracks"),
    path("logout/", views.spotify_logout, name="spotify_logout"),
]
