import requests
import base64
import logging
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta
from .models import SpotifyPlaylist, SpotifyTrack, SpotifyToken

logger = logging.getLogger(__name__)

def is_admin(user):
    """Check if user is admin/staff"""
    return user.is_staff or user.is_superuser

# PUBLIC VIEW - Anyone can see stored playlists
def my_playlist(request):
    """Public view showing stored Spotify playlists"""
    # Get all public playlists from database
    playlists = SpotifyPlaylist.objects.filter(is_public=True)
    
    # Convert to Spotify API format for template compatibility
    playlist_data = {
        'items': [
            {
                'id': playlist.spotify_id,
                'name': playlist.name,
                'description': playlist.description or "",
                'owner': {'display_name': playlist.owner_name},
                'images': [{'url': playlist.image_url}] if playlist.image_url else [],
                'external_urls': {'spotify': playlist.external_url},
                'tracks': {'total': playlist.track_count},
                'last_synced': playlist.last_synced
            }
            for playlist in playlists
        ]
    }
    
    # Check if we have any playlists
    if not playlists.exists():
        # Show demo playlists if no real data
        demo_playlists = {
            'items': [
                {
                    'name': 'Coding Focus 🎯',
                    'owner': {'display_name': 'Roshan Damor'},
                    'images': [{'url': 'https://placehold.co/300x300/1a1a2e/16213e?text=Coding+Focus'}],
                    'external_urls': {'spotify': 'https://open.spotify.com/playlist/demo1'},
                    'description': 'Perfect beats for deep focus coding sessions'
                },
                {
                    'name': 'Late Night Coding 🌙',
                    'owner': {'display_name': 'Roshan Damor'},
                    'images': [{'url': 'https://placehold.co/300x300/0f0f0f/ffd700?text=Late+Night'}],
                    'external_urls': {'spotify': 'https://open.spotify.com/playlist/demo2'},
                    'description': 'Chill vibes for those midnight coding marathons'
                },
                {
                    'name': 'Debugging Chill 🐛',
                    'owner': {'display_name': 'Roshan Damor'},
                    'images': [{'url': 'https://placehold.co/300x300/2c3e50/e74c3c?text=Debug+Chill'}],
                    'external_urls': {'spotify': 'https://open.spotify.com/playlist/demo3'},
                    'description': 'Relaxing tunes to keep you calm while hunting bugs'
                },
                {
                    'name': 'Coffee & Code ☕',
                    'owner': {'display_name': 'Roshan Damor'},
                    'images': [{'url': 'https://placehold.co/300x300/8b4513/deb887?text=Coffee+Code'}],
                    'external_urls': {'spotify': 'https://open.spotify.com/playlist/demo4'},
                    'description': 'Morning energy with your favorite brew'
                },
                {
                    'name': 'Productivity Beats 🚀',
                    'owner': {'display_name': 'Roshan Damor'},
                    'images': [{'url': 'https://placehold.co/300x300/4a90e2/ffffff?text=Productivity'}],
                    'external_urls': {'spotify': 'https://open.spotify.com/playlist/demo5'},
                    'description': 'High-energy tracks to boost your coding productivity'
                },
                {
                    'name': 'Algorithm Vibes 🧮',
                    'owner': {'display_name': 'Roshan Damor'},
                    'images': [{'url': 'https://placehold.co/300x300/27ae60/ffffff?text=Algorithm'}],
                    'external_urls': {'spotify': 'https://open.spotify.com/playlist/demo6'},
                    'description': 'Complex rhythms for complex algorithms'
                }
            ]
        }
        return render(request, "music/playlist.html", {
            "playlists": demo_playlists, 
            "is_demo": True,
            "show_admin_sync": request.user.is_staff if request.user.is_authenticated else False,
            "admin_note": "Admin: Connect Spotify to sync real playlists" if request.user.is_staff else None
        })
    
    return render(request, "music/playlist.html", {
        "playlists": playlist_data, 
        "is_demo": False,
        "show_admin_sync": request.user.is_staff if request.user.is_authenticated else False,
        "last_sync": playlists.first().last_synced if playlists.exists() else None
    })

# ADMIN ONLY - Sync playlists from Spotify
@login_required
@user_passes_test(is_admin)
def admin_spotify_sync(request):
    """Admin view to sync playlists from Spotify"""
    # Check if we have valid tokens
    try:
        token_obj = SpotifyToken.objects.latest('created_at')
        if token_obj.is_expired():
            # Try to refresh token
            if not refresh_spotify_token(token_obj):
                messages.error(request, "Spotify token expired and refresh failed. Please re-authenticate.")
                return redirect("admin_spotify_login")
            token_obj.refresh_from_db()
        
        access_token = token_obj.access_token
    except SpotifyToken.DoesNotExist:
        messages.error(request, "No Spotify authentication found. Please connect your Spotify account first.")
        return redirect("admin_spotify_login")
    
    # Fetch and sync playlists
    try:
        playlists_synced = sync_spotify_playlists(access_token)
        messages.success(request, f"Successfully synced {playlists_synced} playlists from Spotify!")
    except Exception as e:
        logger.error(f"Playlist sync failed: {str(e)}")
        messages.error(request, f"Playlist sync failed: {str(e)}")
    
    return redirect("my_playlist")

# ADMIN ONLY - Spotify authentication
@login_required
@user_passes_test(is_admin)
def admin_spotify_login(request):
    """Admin Spotify authentication"""
    scopes = "user-read-private user-read-email playlist-read-private playlist-read-collaborative"
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?response_type=code&client_id={settings.SPOTIFY_CLIENT_ID}"
        f"&scope={scopes}&redirect_uri={settings.SPOTIFY_REDIRECT_URI}"
        "&show_dialog=true"  # Force re-auth for admin
    )
    return redirect(auth_url)

# ADMIN ONLY - Spotify callback handler
@login_required
@user_passes_test(is_admin)
def admin_spotify_callback(request):
    """Handle Spotify OAuth callback for admin"""
    code = request.GET.get("code")
    error = request.GET.get("error")
    
    if error:
        logger.error(f"Spotify OAuth error: {error}")
        messages.error(request, f"Spotify authentication failed: {error}")
        return redirect("my_playlist")
    
    if not code:
        logger.error("No authorization code received from Spotify")
        messages.error(request, "No authorization code received from Spotify")
        return redirect("my_playlist")
    
    token_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(
        f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}".encode()
    ).decode("utf-8")

    try:
        response = requests.post(
            token_url,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
            },
            headers={"Authorization": f"Basic {auth_header}"},
        )
        response.raise_for_status()

        token_data = response.json()
        logger.info(f"Successfully obtained Spotify token for admin {request.user.username}")

        # Store tokens in database for admin use
        SpotifyToken.objects.create(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data.get("expires_in", 3600),
            scope=token_data.get("scope", ""),
            token_type=token_data.get("token_type", "Bearer")
        )
        
        messages.success(request, "Successfully connected to Spotify! You can now sync your playlists.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to exchange code for token: {str(e)}")
        messages.error(request, "Failed to authenticate with Spotify. Please try again.")
        return redirect("my_playlist")

    return redirect("admin_spotify_sync")

# Helper function to refresh Spotify token
def refresh_spotify_token(token_obj):
    """Refresh an expired Spotify token"""
    if not token_obj.refresh_token:
        return False
    
    token_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(
        f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}".encode()
    ).decode("utf-8")

    try:
        response = requests.post(
            token_url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": token_obj.refresh_token,
            },
            headers={"Authorization": f"Basic {auth_header}"},
        )
        response.raise_for_status()

        token_data = response.json()
        
        # Update existing token
        token_obj.access_token = token_data["access_token"]
        token_obj.expires_at = timezone.now() + timedelta(seconds=token_data.get("expires_in", 3600))
        if "refresh_token" in token_data:
            token_obj.refresh_token = token_data["refresh_token"]
        token_obj.save()
        
        logger.info("Successfully refreshed Spotify token")
        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to refresh Spotify token: {str(e)}")
        return False

# Helper function to sync playlists from Spotify API
def sync_spotify_playlists(access_token):
    """Sync playlists from Spotify API to database"""
    try:
        response = requests.get(
            "https://api.spotify.com/v1/me/playlists",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"limit": 50}
        )
        response.raise_for_status()
        
        playlists_data = response.json()
        synced_count = 0
        
        for playlist in playlists_data.get('items', []):
            # Get track count for this playlist
            tracks_response = requests.get(
                f"https://api.spotify.com/v1/playlists/{playlist['id']}/tracks",
                headers={"Authorization": f"Bearer {access_token}"},
                params={"limit": 1}  # Just to get total count
            )
            tracks_response.raise_for_status()
            track_count = tracks_response.json().get('total', 0)
            
            # Update or create playlist
            spotify_playlist, created = SpotifyPlaylist.objects.update_or_create(
                spotify_id=playlist['id'],
                defaults={
                    'name': playlist['name'],
                    'description': playlist.get('description', ''),
                    'owner_name': playlist['owner']['display_name'],
                    'image_url': playlist['images'][0]['url'] if playlist['images'] else None,
                    'external_url': playlist['external_urls']['spotify'],
                    'track_count': track_count,
                    'last_synced': timezone.now(),
                    'is_public': True  # Make all synced playlists public by default
                }
            )
            
            synced_count += 1
            logger.info(f"{'Created' if created else 'Updated'} playlist: {playlist['name']}")
        
        return synced_count

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to sync playlists: {str(e)}")
        raise Exception(f"Failed to sync playlists: {str(e)}")

# API endpoint for playlist tracks (AJAX)
def get_playlist_tracks(request, playlist_id):
    """Get tracks for a specific playlist"""
    try:
        playlist = SpotifyPlaylist.objects.get(spotify_id=playlist_id)
        tracks = SpotifyTrack.objects.filter(playlist=playlist)
        
        tracks_data = {
            'tracks': [
                {
                    'name': track.name,
                    'artist': track.artist,
                    'album': track.album,
                    'duration_ms': track.duration_ms,
                    'preview_url': track.preview_url,
                    'external_url': track.external_url,
                    'image_url': track.image_url
                }
                for track in tracks
            ],
            'total': tracks.count()
        }
        
        return JsonResponse(tracks_data)
    
    except SpotifyPlaylist.DoesNotExist:
        return JsonResponse({'error': 'Playlist not found'}, status=404)
    except Exception as e:
        logger.error(f"Error fetching tracks for playlist {playlist_id}: {str(e)}")
        return JsonResponse({'error': 'Failed to fetch tracks'}, status=500)

# Legacy support - redirect old URLs to new system
def spotify_login(request):
    """Redirect to admin login if user is admin, otherwise show info"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_spotify_login")
    else:
        messages.info(request, "Playlists are publicly available. No login required!")
        return redirect("my_playlist")

def spotify_callback(request):
    """Redirect old callback to admin callback"""
    if request.user.is_authenticated and request.user.is_staff:
        return admin_spotify_callback(request)
    else:
        return redirect("my_playlist")

def playlist_tracks(request, playlist_id):
    """Alias for get_playlist_tracks for backward compatibility"""
    return get_playlist_tracks(request, playlist_id)

def spotify_logout(request):
    """No longer needed - redirect to playlist page"""
    messages.info(request, "No logout needed - playlists are public!")
    return redirect("my_playlist")
