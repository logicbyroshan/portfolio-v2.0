from django.db import models
from django.utils import timezone

class SpotifyPlaylist(models.Model):
    spotify_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    external_url = models.URLField()
    owner_name = models.CharField(max_length=255)
    track_count = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_synced = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Spotify Playlist"
        verbose_name_plural = "Spotify Playlists"
    
    def __str__(self):
        return self.name

class SpotifyTrack(models.Model):
    playlist = models.ForeignKey(SpotifyPlaylist, related_name='tracks', on_delete=models.CASCADE)
    spotify_id = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, blank=True)
    duration_ms = models.IntegerField(default=0)
    preview_url = models.URLField(blank=True, null=True)
    external_url = models.URLField()
    track_number = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['track_number']
        unique_together = ['playlist', 'spotify_id']
        verbose_name = "Spotify Track"
        verbose_name_plural = "Spotify Tracks"
    
    def __str__(self):
        return f"{self.name} by {self.artist}"

class SpotifyToken(models.Model):
    """Store admin's Spotify tokens for periodic sync"""
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Spotify Token"
        verbose_name_plural = "Spotify Tokens"
    
    def __str__(self):
        return f"Spotify Token (expires: {self.expires_at})"
    
    def is_expired(self):
        return timezone.now() >= self.expires_at
