from django.urls import path
from . import views

urlpatterns = [
    path("spotify-login/", views.spotify_login, name="spotify_login"),
    path("my-playlist/", views.my_playlist, name="my_playlist"),
    path("playlist/<str:playlist_id>/tracks/", views.playlist_tracks, name="playlist_tracks"),
    path("logout/", views.spotify_logout, name="spotify_logout"),
    path("debug/", views.spotify_debug, name="spotify_debug"),
    path("test/", views.spotify_test, name="spotify_test"),
]
