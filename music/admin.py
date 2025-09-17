from django.contrib import admin
from .models import SpotifyPlaylist, SpotifyTrack, SpotifyToken

@admin.register(SpotifyPlaylist)
class SpotifyPlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_name', 'track_count', 'is_public', 'last_synced')
    list_filter = ('is_public', 'owner_name', 'last_synced')
    search_fields = ('name', 'description', 'owner_name')
    readonly_fields = ('spotify_id', 'external_url', 'created_at', 'updated_at', 'last_synced')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'owner_name')
        }),
        ('Spotify Data', {
            'fields': ('spotify_id', 'external_url', 'image_url', 'track_count', 'is_public')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_synced'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SpotifyTrack)
class SpotifyTrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'album', 'playlist', 'track_number')
    list_filter = ('playlist', 'artist')
    search_fields = ('name', 'artist', 'album')
    readonly_fields = ('spotify_id', 'external_url', 'duration_ms', 'preview_url')
    
    fieldsets = (
        ('Track Information', {
            'fields': ('name', 'artist', 'album', 'track_number')
        }),
        ('Playlist', {
            'fields': ('playlist',)
        }),
        ('Spotify Data', {
            'fields': ('spotify_id', 'external_url', 'duration_ms', 'preview_url')
        }),
    )

@admin.register(SpotifyToken)
class SpotifyTokenAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'expires_at', 'is_expired')
    readonly_fields = ('access_token', 'refresh_token', 'expires_at', 'created_at')
    
    def is_expired(self, obj):
        from django.utils import timezone
        return timezone.now() >= obj.expires_at
    is_expired.boolean = True
    is_expired.short_description = 'Expired'
    
    def has_add_permission(self, request):
        # Prevent manual token creation through admin
        return False
