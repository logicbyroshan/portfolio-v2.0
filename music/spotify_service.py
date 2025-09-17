# music/spotify_service.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings
from django.utils import timezone
from .models import SpotifyPlaylist, SpotifyTrack, SpotifyToken
import logging

logger = logging.getLogger(__name__)

class SpotifyService:
    def __init__(self):
        """Initialize Spotify service with credentials"""
        self.client_id = getattr(settings, 'SPOTIFY_CLIENT_ID', '')
        self.client_secret = getattr(settings, 'SPOTIFY_CLIENT_SECRET', '')
        self.redirect_uri = getattr(settings, 'SPOTIFY_REDIRECT_URI', 'http://localhost:8000/callback/')
        
        if not all([self.client_id, self.client_secret]):
            raise ValueError("Spotify credentials not configured in settings")
        
        self.scope = "playlist-read-private playlist-read-collaborative"
        self.sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope
        )
        self.sp = None
    
    def get_auth_url(self):
        """Get Spotify authorization URL for initial setup"""
        return self.sp_oauth.get_authorize_url()
    
    def authenticate_with_code(self, code):
        """Authenticate using authorization code"""
        try:
            token_info = self.sp_oauth.get_access_token(code)
            self.save_token(token_info)
            return True
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False
    
    def save_token(self, token_info):
        """Save token to database"""
        SpotifyToken.objects.all().delete()  # Keep only latest token
        
        expires_at = timezone.now() + timezone.timedelta(seconds=token_info['expires_in'])
        
        SpotifyToken.objects.create(
            access_token=token_info['access_token'],
            refresh_token=token_info['refresh_token'],
            expires_at=expires_at
        )
    
    def get_spotify_client(self):
        """Get authenticated Spotify client"""
        if self.sp:
            return self.sp
        
        # Get token from database
        token_obj = SpotifyToken.objects.first()
        if not token_obj:
            raise ValueError("No Spotify token found. Please authenticate first.")
        
        # Check if token is expired
        if timezone.now() >= token_obj.expires_at:
            # Refresh token
            token_info = self.sp_oauth.refresh_access_token(token_obj.refresh_token)
            self.save_token(token_info)
            token_obj.refresh_from_db()
        
        # Create Spotify client
        self.sp = spotipy.Spotify(auth=token_obj.access_token)
        return self.sp
    
    def sync_playlists(self):
        """Sync all playlists from Spotify"""
        try:
            sp = self.get_spotify_client()
            
            # Get current user
            user = sp.current_user()
            user_id = user['id']
            logger.info(f"Syncing playlists for user: {user['display_name']}")
            
            # Get all playlists
            playlists = []
            offset = 0
            limit = 50
            
            while True:
                results = sp.user_playlists(user_id, offset=offset, limit=limit)
                playlists.extend(results['items'])
                
                if len(results['items']) < limit:
                    break
                offset += limit
            
            synced_count = 0
            
            for playlist_data in playlists:
                if playlist_data is None:
                    continue
                    
                # Skip if not owned by user (collaborative playlists)
                if playlist_data['owner']['id'] != user_id:
                    continue
                
                playlist, created = self.sync_single_playlist(playlist_data)
                if playlist:
                    synced_count += 1
                    if created:
                        logger.info(f"Created new playlist: {playlist.name}")
                    else:
                        logger.info(f"Updated playlist: {playlist.name}")
            
            logger.info(f"Successfully synced {synced_count} playlists")
            return synced_count
            
        except Exception as e:
            logger.error(f"Failed to sync playlists: {e}")
            raise
    
    def sync_single_playlist(self, playlist_data):
        """Sync a single playlist"""
        try:
            sp = self.get_spotify_client()
            
            # Get playlist details
            playlist_id = playlist_data['id']
            
            # Get or create playlist
            playlist, created = SpotifyPlaylist.objects.get_or_create(
                spotify_id=playlist_id,
                defaults={
                    'name': playlist_data['name'],
                    'description': playlist_data.get('description', ''),
                    'image_url': playlist_data['images'][0]['url'] if playlist_data['images'] else '',
                    'external_url': playlist_data['external_urls']['spotify'],
                    'owner_name': playlist_data['owner']['display_name'],
                    'track_count': playlist_data['tracks']['total'],
                    'is_public': playlist_data['public']
                }
            )
            
            # Update existing playlist
            if not created:
                playlist.name = playlist_data['name']
                playlist.description = playlist_data.get('description', '')
                playlist.image_url = playlist_data['images'][0]['url'] if playlist_data['images'] else ''
                playlist.track_count = playlist_data['tracks']['total']
                playlist.is_public = playlist_data['public']
                playlist.save()
            
            # Sync tracks
            self.sync_playlist_tracks(playlist, playlist_id)
            
            # Update last synced time
            playlist.last_synced = timezone.now()
            playlist.save()
            
            return playlist, created
            
        except Exception as e:
            logger.error(f"Failed to sync playlist {playlist_data.get('name', 'Unknown')}: {e}")
            return None, False
    
    def sync_playlist_tracks(self, playlist, playlist_id):
        """Sync tracks for a specific playlist"""
        try:
            sp = self.get_spotify_client()
            
            # Clear existing tracks
            playlist.tracks.all().delete()
            
            # Get all tracks
            tracks = []
            offset = 0
            limit = 100
            
            while True:
                results = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
                tracks.extend(results['items'])
                
                if len(results['items']) < limit:
                    break
                offset += limit
            
            # Create track objects
            track_objects = []
            for i, track_item in enumerate(tracks):
                if track_item is None or track_item['track'] is None:
                    continue
                
                track_data = track_item['track']
                
                # Skip non-music tracks (podcasts, etc.)
                if track_data['type'] != 'track':
                    continue
                
                # Get artist names
                artists = [artist['name'] for artist in track_data['artists']]
                artist_string = ', '.join(artists)
                
                track_obj = SpotifyTrack(
                    playlist=playlist,
                    spotify_id=track_data['id'],
                    name=track_data['name'],
                    artist=artist_string,
                    album=track_data['album']['name'] if track_data['album'] else '',
                    duration_ms=track_data['duration_ms'],
                    preview_url=track_data.get('preview_url', ''),
                    external_url=track_data['external_urls']['spotify'],
                    track_number=i + 1
                )
                track_objects.append(track_obj)
            
            # Bulk create tracks
            SpotifyTrack.objects.bulk_create(track_objects, ignore_conflicts=True)
            
            # Update track count
            playlist.track_count = len(track_objects)
            playlist.save()
            
            logger.info(f"Synced {len(track_objects)} tracks for playlist: {playlist.name}")
            
        except Exception as e:
            logger.error(f"Failed to sync tracks for playlist {playlist.name}: {e}")
    
    def get_user_info(self):
        """Get current user information"""
        try:
            sp = self.get_spotify_client()
            return sp.current_user()
        except Exception as e:
            logger.error(f"Failed to get user info: {e}")
            return None