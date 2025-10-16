# Admin registrations for music app models are handled in roshan app
# to avoid duplicate registrations that cause 500 errors in admin panel

from django.contrib import admin

# Note: SpotifyPlaylist, SpotifyTrack, and SpotifyToken models are registered
# in roshan/admin.py to maintain consistency and avoid conflicts
