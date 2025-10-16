import requests
import base64
import logging
import json
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
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
        "items": [
            {
                "id": playlist.spotify_id,
                "name": playlist.name,
                "description": playlist.description or "",
                "owner": {"display_name": playlist.owner_name},
                "images": [{"url": playlist.image_url}] if playlist.image_url else [],
                "external_urls": {"spotify": playlist.external_url},
                "tracks": {"total": playlist.track_count},
                "last_synced": playlist.last_synced,
            }
            for playlist in playlists
        ]
    }

    # Check if we have any playlists
    if not playlists.exists():
        # Show demo playlists if no real data with sample audio
        demo_playlists = {
            "items": [
                {
                    "id": "demo1",
                    "name": "Coding Focus 🎯",
                    "owner": {"display_name": "Roshan Damor"},
                    "images": [
                        {
                            "url": "https://placehold.co/300x300/1a1a2e/16213e?text=Coding+Focus"
                        }
                    ],
                    "external_urls": {
                        "spotify": "https://open.spotify.com/playlist/demo1"
                    },
                    "description": "Perfect beats for deep focus coding sessions",
                    "tracks": {"total": 5},
                },
                {
                    "id": "demo2",
                    "name": "Late Night Coding 🌙",
                    "owner": {"display_name": "Roshan Damor"},
                    "images": [
                        {
                            "url": "https://placehold.co/300x300/0f0f0f/ffd700?text=Late+Night"
                        }
                    ],
                    "external_urls": {
                        "spotify": "https://open.spotify.com/playlist/demo2"
                    },
                    "description": "Chill vibes for those midnight coding marathons",
                    "tracks": {"total": 6},
                },
                {
                    "id": "demo3",
                    "name": "Debugging Chill 🐛",
                    "owner": {"display_name": "Roshan Damor"},
                    "images": [
                        {
                            "url": "https://placehold.co/300x300/2c3e50/e74c3c?text=Debug+Chill"
                        }
                    ],
                    "external_urls": {
                        "spotify": "https://open.spotify.com/playlist/demo3"
                    },
                    "description": "Relaxing tunes to keep you calm while hunting bugs",
                    "tracks": {"total": 4},
                },
                {
                    "id": "demo4",
                    "name": "Coffee & Code ☕",
                    "owner": {"display_name": "Roshan Damor"},
                    "images": [
                        {
                            "url": "https://placehold.co/300x300/8b4513/deb887?text=Coffee+Code"
                        }
                    ],
                    "external_urls": {
                        "spotify": "https://open.spotify.com/playlist/demo4"
                    },
                    "description": "Morning energy with your favorite brew",
                    "tracks": {"total": 7},
                },
                {
                    "id": "demo5",
                    "name": "Productivity Beats 🚀",
                    "owner": {"display_name": "Roshan Damor"},
                    "images": [
                        {
                            "url": "https://placehold.co/300x300/4a90e2/ffffff?text=Productivity"
                        }
                    ],
                    "external_urls": {
                        "spotify": "https://open.spotify.com/playlist/demo5"
                    },
                    "description": "High-energy tracks to boost your coding productivity",
                    "tracks": {"total": 8},
                },
                {
                    "id": "demo6",
                    "name": "Algorithm Vibes 🧮",
                    "owner": {"display_name": "Roshan Damor"},
                    "images": [
                        {
                            "url": "https://placehold.co/300x300/27ae60/ffffff?text=Algorithm"
                        }
                    ],
                    "external_urls": {
                        "spotify": "https://open.spotify.com/playlist/demo6"
                    },
                    "description": "Complex rhythms for complex algorithms",
                    "tracks": {"total": 5},
                },
            ]
        }
        return render(
            request,
            "music/playlist.html",
            {
                "playlists": demo_playlists,
                "is_demo": True,
                "show_admin_sync": (
                    request.user.is_staff if request.user.is_authenticated else False
                ),
                "admin_note": (
                    "Admin: Connect Spotify to sync real playlists"
                    if request.user.is_staff
                    else None
                ),
            },
        )

    return render(
        request,
        "music/playlist.html",
        {
            "playlists": playlist_data,
            "is_demo": False,
            "show_admin_sync": (
                request.user.is_staff if request.user.is_authenticated else False
            ),
            "last_sync": playlists.first().last_synced if playlists.exists() else None,
        },
    )


# Playlist Detail View
def playlist_detail(request, playlist_id):
    """Detailed view of a specific playlist with tracks"""

    # Handle demo playlists
    if playlist_id.startswith("demo"):
        demo_tracks = generate_demo_tracks_for_detail(playlist_id)
        demo_playlist = get_demo_playlist_info(playlist_id)

        # Format tracks for template
        formatted_tracks = []
        for i, track in enumerate(demo_tracks):
            formatted_tracks.append(
                {
                    "name": track["name"],
                    "artist": track["artist"],
                    "album": track.get("album", "Demo Album"),
                    "duration_ms": track["duration_ms"],
                    "duration_formatted": format_duration(track["duration_ms"]),
                    "preview_url": track["preview_url"],
                    "external_url": f"https://open.spotify.com/track/demo{i+1}",
                    "track_number": i + 1,
                }
            )

        # Serialize tracks for JavaScript
        tracks_json = json.dumps(
            [
                {
                    "name": track["name"],
                    "artist": track["artist"],
                    "album": track["album"],
                    "duration_ms": track["duration_ms"],
                    "preview_url": track["preview_url"],
                    "external_url": track["external_url"],
                }
                for track in formatted_tracks
            ]
        )

        return render(
            request,
            "music/playlist_detail.html",
            {
                "playlist": demo_playlist,
                "tracks": formatted_tracks,
                "tracks_json": tracks_json,
                "is_demo": True,
            },
        )

    # Handle real playlists
    try:
        playlist = SpotifyPlaylist.objects.get(spotify_id=playlist_id)
        tracks = SpotifyTrack.objects.filter(playlist=playlist).order_by("track_number")

        # Format tracks for template
        formatted_tracks = []
        for track in tracks:
            formatted_tracks.append(
                {
                    "name": track.name,
                    "artist": track.artist,
                    "album": track.album or "Unknown Album",
                    "duration_ms": track.duration_ms,
                    "duration_formatted": format_duration(track.duration_ms),
                    "preview_url": track.preview_url,
                    "external_url": track.external_url,
                    "track_number": track.track_number,
                }
            )

        # Serialize tracks for JavaScript
        tracks_json = json.dumps(
            [
                {
                    "name": track["name"],
                    "artist": track["artist"],
                    "album": track["album"],
                    "duration_ms": track["duration_ms"],
                    "preview_url": track["preview_url"],
                    "external_url": track["external_url"],
                }
                for track in formatted_tracks
            ]
        )

        # Calculate total duration
        total_duration_ms = sum(track.duration_ms for track in tracks)
        total_duration = format_duration(total_duration_ms)

        playlist_data = {
            "id": playlist.spotify_id,
            "name": playlist.name,
            "description": playlist.description,
            "owner_name": playlist.owner_name,
            "image_url": playlist.image_url,
            "external_url": playlist.external_url,
            "track_count": tracks.count(),
            "total_duration": total_duration,
        }

        return render(
            request,
            "music/playlist_detail.html",
            {
                "playlist": playlist_data,
                "tracks": formatted_tracks,
                "tracks_json": tracks_json,
                "is_demo": False,
            },
        )

    except SpotifyPlaylist.DoesNotExist:
        messages.error(request, "Playlist not found.")
        return redirect("my_playlist")


# ADMIN ONLY - Sync playlists from Spotify
@login_required
@user_passes_test(is_admin)
def admin_spotify_sync(request):
    """Admin view to sync playlists from Spotify"""
    # Check if we have valid tokens
    try:
        token_obj = SpotifyToken.objects.latest("created_at")
        if token_obj.is_expired():
            # Try to refresh token
            if not refresh_spotify_token(token_obj):
                messages.error(
                    request,
                    "Spotify token expired and refresh failed. Please re-authenticate.",
                )
                return redirect("admin_spotify_login")
            token_obj.refresh_from_db()

        access_token = token_obj.access_token
    except SpotifyToken.DoesNotExist:
        messages.error(
            request,
            "No Spotify authentication found. Please connect your Spotify account first.",
        )
        return redirect("admin_spotify_login")

    # Fetch and sync playlists
    try:
        playlists_synced = sync_spotify_playlists(access_token)
        messages.success(
            request, f"Successfully synced {playlists_synced} playlists from Spotify!"
        )
    except Exception as e:
        # Sanitize error message to prevent log injection
        safe_error = str(e).replace("\n", "\\n").replace("\r", "\\r")[:200]
        logger.error(f"Playlist sync failed: {safe_error}")
        # Don't show detailed error to user for security
        messages.error(request, "Playlist sync failed. Please try again later.")

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
        # Sanitize error parameter to prevent log injection
        safe_error = str(error).replace("\n", "\\n").replace("\r", "\\r")[:100]
        logger.error(f"Spotify OAuth error: {safe_error}")
        # Also sanitize for user display
        safe_error_display = str(error)[:50] if error else "Unknown error"
        messages.error(request, f"Spotify authentication failed: {safe_error_display}")
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
        logger.info(
            f"Successfully obtained Spotify token for admin {request.user.username}"
        )

        # Store tokens in database for admin use
        SpotifyToken.objects.create(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            expires_in=token_data.get("expires_in", 3600),
            scope=token_data.get("scope", ""),
            token_type=token_data.get("token_type", "Bearer"),
        )

        messages.success(
            request,
            "Successfully connected to Spotify! You can now sync your playlists.",
        )

    except requests.exceptions.RequestException as e:
        # Sanitize error message to prevent log injection
        safe_error = str(e).replace("\n", "\\n").replace("\r", "\\r")[:200]
        logger.error(f"Failed to exchange code for token: {safe_error}")
        messages.error(
            request, "Failed to authenticate with Spotify. Please try again."
        )
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
        token_obj.expires_at = timezone.now() + timedelta(
            seconds=token_data.get("expires_in", 3600)
        )
        if "refresh_token" in token_data:
            token_obj.refresh_token = token_data["refresh_token"]
        token_obj.save()

        logger.info("Successfully refreshed Spotify token")
        return True

    except requests.exceptions.RequestException as e:
        # Sanitize error message to prevent log injection
        safe_error = str(e).replace("\n", "\\n").replace("\r", "\\r")[:200]
        logger.error(f"Failed to refresh Spotify token: {safe_error}")
        return False


# Helper function to sync playlists from Spotify API
def sync_spotify_playlists(access_token):
    """Sync playlists from Spotify API to database"""
    try:
        response = requests.get(
            "https://api.spotify.com/v1/me/playlists",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"limit": 50},
        )
        response.raise_for_status()

        playlists_data = response.json()
        synced_count = 0

        for playlist in playlists_data.get("items", []):
            # Get track count for this playlist
            tracks_response = requests.get(
                f"https://api.spotify.com/v1/playlists/{playlist['id']}/tracks",
                headers={"Authorization": f"Bearer {access_token}"},
                params={"limit": 1},  # Just to get total count
            )
            tracks_response.raise_for_status()
            track_count = tracks_response.json().get("total", 0)

            # Update or create playlist
            spotify_playlist, created = SpotifyPlaylist.objects.update_or_create(
                spotify_id=playlist["id"],
                defaults={
                    "name": playlist["name"],
                    "description": playlist.get("description", ""),
                    "owner_name": playlist["owner"]["display_name"],
                    "image_url": (
                        playlist["images"][0]["url"] if playlist["images"] else None
                    ),
                    "external_url": playlist["external_urls"]["spotify"],
                    "track_count": track_count,
                    "last_synced": timezone.now(),
                    "is_public": True,  # Make all synced playlists public by default
                },
            )

            synced_count += 1
            logger.info(
                f"{'Created' if created else 'Updated'} playlist: {playlist['name']}"
            )

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
            "tracks": [
                {
                    "name": track.name,
                    "artist": track.artist,
                    "album": track.album,
                    "duration_ms": track.duration_ms,
                    "preview_url": track.preview_url,
                    "external_url": track.external_url,
                }
                for track in tracks
            ],
            "total": tracks.count(),
        }

        return JsonResponse(tracks_data)

    except SpotifyPlaylist.DoesNotExist:
        return JsonResponse({"error": "Playlist not found"}, status=404)
    except Exception as e:
        logger.error(f"Error fetching tracks for playlist {playlist_id}: {str(e)}")
        return JsonResponse({"error": "Failed to fetch tracks"}, status=500)


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


# Helper functions
def format_duration(duration_ms):
    """Format duration from milliseconds to MM:SS format"""
    if not duration_ms:
        return "0:00"

    total_seconds = duration_ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return f"{minutes}:{seconds:02d}"


def get_demo_playlist_info(playlist_id):
    """Get demo playlist information"""
    demo_playlists = {
        "demo1": {
            "id": "demo1",
            "name": "Coding Focus 🎯",
            "description": "Perfect beats for deep focus coding sessions",
            "owner_name": "Roshan Damor",
            "image_url": "https://placehold.co/300x300/1a1a2e/16213e?text=Coding+Focus",
            "external_url": "https://open.spotify.com/playlist/demo1",
        },
        "demo2": {
            "id": "demo2",
            "name": "Late Night Coding 🌙",
            "description": "Chill vibes for those midnight coding marathons",
            "owner_name": "Roshan Damor",
            "image_url": "https://placehold.co/300x300/0f0f0f/ffd700?text=Late+Night",
            "external_url": "https://open.spotify.com/playlist/demo2",
        },
        "demo3": {
            "id": "demo3",
            "name": "Debugging Chill 🐛",
            "description": "Relaxing tunes to keep you calm while hunting bugs",
            "owner_name": "Roshan Damor",
            "image_url": "https://placehold.co/300x300/2c3e50/e74c3c?text=Debug+Chill",
            "external_url": "https://open.spotify.com/playlist/demo3",
        },
        "demo4": {
            "id": "demo4",
            "name": "Coffee & Code ☕",
            "description": "Morning energy with your favorite brew",
            "owner_name": "Roshan Damor",
            "image_url": "https://placehold.co/300x300/8b4513/deb887?text=Coffee+Code",
            "external_url": "https://open.spotify.com/playlist/demo4",
        },
        "demo5": {
            "id": "demo5",
            "name": "Productivity Beats 🚀",
            "description": "High-energy tracks to boost your coding productivity",
            "owner_name": "Roshan Damor",
            "image_url": "https://placehold.co/300x300/4a90e2/ffffff?text=Productivity",
            "external_url": "https://open.spotify.com/playlist/demo5",
        },
        "demo6": {
            "id": "demo6",
            "name": "Algorithm Vibes 🧮",
            "description": "Complex rhythms for complex algorithms",
            "owner_name": "Roshan Damor",
            "image_url": "https://placehold.co/300x300/27ae60/ffffff?text=Algorithm",
            "external_url": "https://open.spotify.com/playlist/demo6",
        },
    }

    return demo_playlists.get(playlist_id, demo_playlists["demo1"])


def generate_demo_tracks_for_detail(playlist_id):
    """Generate detailed demo tracks for playlist detail view"""
    track_sets = {
        "demo1": [
            {
                "name": "Code Flow",
                "artist": "Dev Beats",
                "album": "Productivity Sessions",
                "duration_ms": 210000,
                "preview_url": "demo",
            },
            {
                "name": "Algorithm Dreams",
                "artist": "Binary Rhythms",
                "album": "Logic Loops",
                "duration_ms": 195000,
                "preview_url": "demo",
            },
            {
                "name": "Syntax Smooth",
                "artist": "Logic Loop",
                "album": "Code Compilation",
                "duration_ms": 225000,
                "preview_url": None,
            },
            {
                "name": "Debug Mode",
                "artist": "Error Collective",
                "album": "Fix & Flow",
                "duration_ms": 180000,
                "preview_url": "demo",
            },
            {
                "name": "Compile Time",
                "artist": "Function Flow",
                "album": "Build Process",
                "duration_ms": 240000,
                "preview_url": None,
            },
        ],
        "demo2": [
            {
                "name": "Midnight Variables",
                "artist": "Late Night Logic",
                "album": "After Hours",
                "duration_ms": 220000,
                "preview_url": "demo",
            },
            {
                "name": "Coffee Loop",
                "artist": "Caffeine Code",
                "album": "Brew & Build",
                "duration_ms": 205000,
                "preview_url": None,
            },
            {
                "name": "Silent Debugging",
                "artist": "Quiet Quarters",
                "album": "Peaceful Programming",
                "duration_ms": 190000,
                "preview_url": "demo",
            },
            {
                "name": "Terminal Dreams",
                "artist": "Command Line",
                "album": "Shell Scripts",
                "duration_ms": 235000,
                "preview_url": None,
            },
            {
                "name": "Empty Strings",
                "artist": "Null Pointer",
                "album": "Memory Management",
                "duration_ms": 200000,
                "preview_url": "demo",
            },
            {
                "name": "Async Await",
                "artist": "Promise Resolve",
                "album": "Concurrent Computing",
                "duration_ms": 215000,
                "preview_url": None,
            },
        ],
        "demo3": [
            {
                "name": "Bug Hunt",
                "artist": "Debug Masters",
                "album": "Error Tracking",
                "duration_ms": 195000,
                "preview_url": "demo",
            },
            {
                "name": "Exception Handler",
                "artist": "Try Catch",
                "album": "Error Management",
                "duration_ms": 210000,
                "preview_url": None,
            },
            {
                "name": "Stack Trace",
                "artist": "Error Log",
                "album": "Debugging Tools",
                "duration_ms": 185000,
                "preview_url": "demo",
            },
            {
                "name": "Memory Leak",
                "artist": "Performance Fix",
                "album": "Optimization",
                "duration_ms": 225000,
                "preview_url": None,
            },
        ],
        "demo4": [
            {
                "name": "Morning Commit",
                "artist": "Git Flow",
                "album": "Version Control",
                "duration_ms": 200000,
                "preview_url": "demo",
            },
            {
                "name": "Espresso Logic",
                "artist": "Caffeine Driven",
                "album": "Coffee Code",
                "duration_ms": 190000,
                "preview_url": None,
            },
            {
                "name": "Fresh Branch",
                "artist": "Version Control",
                "album": "Git Workflow",
                "duration_ms": 215000,
                "preview_url": "demo",
            },
            {
                "name": "Pull Request",
                "artist": "Code Review",
                "album": "Collaboration",
                "duration_ms": 205000,
                "preview_url": None,
            },
            {
                "name": "Merge Conflict",
                "artist": "Resolution Squad",
                "album": "Problem Solving",
                "duration_ms": 220000,
                "preview_url": "demo",
            },
            {
                "name": "Deploy Friday",
                "artist": "CI/CD Pipeline",
                "album": "Release Management",
                "duration_ms": 240000,
                "preview_url": None,
            },
            {
                "name": "Weekend Hotfix",
                "artist": "Emergency Patch",
                "album": "Crisis Management",
                "duration_ms": 180000,
                "preview_url": "demo",
            },
        ],
        "demo5": [
            {
                "name": "Sprint Start",
                "artist": "Agile Beats",
                "album": "Scrum Sessions",
                "duration_ms": 210000,
                "preview_url": "demo",
            },
            {
                "name": "Velocity High",
                "artist": "Scrum Master",
                "album": "Team Dynamics",
                "duration_ms": 195000,
                "preview_url": None,
            },
            {
                "name": "Stand Up Meeting",
                "artist": "Daily Sync",
                "album": "Communication",
                "duration_ms": 185000,
                "preview_url": "demo",
            },
            {
                "name": "Backlog Refined",
                "artist": "Story Points",
                "album": "Planning Poker",
                "duration_ms": 220000,
                "preview_url": None,
            },
            {
                "name": "Demo Day",
                "artist": "Show & Tell",
                "album": "Presentation Skills",
                "duration_ms": 235000,
                "preview_url": "demo",
            },
            {
                "name": "Retrospective",
                "artist": "Improvement Loop",
                "album": "Continuous Learning",
                "duration_ms": 200000,
                "preview_url": None,
            },
            {
                "name": "Technical Debt",
                "artist": "Refactor Time",
                "album": "Code Quality",
                "duration_ms": 250000,
                "preview_url": "demo",
            },
            {
                "name": "Production Ready",
                "artist": "Release Candidate",
                "album": "Go Live",
                "duration_ms": 215000,
                "preview_url": None,
            },
        ],
        "demo6": [
            {
                "name": "Binary Search",
                "artist": "O(log n)",
                "album": "Algorithm Anthology",
                "duration_ms": 190000,
                "preview_url": "demo",
            },
            {
                "name": "Quick Sort",
                "artist": "Divide & Conquer",
                "album": "Sorting Solutions",
                "duration_ms": 205000,
                "preview_url": None,
            },
            {
                "name": "Dynamic Programming",
                "artist": "Memoization",
                "album": "Optimization Techniques",
                "duration_ms": 225000,
                "preview_url": "demo",
            },
            {
                "name": "Graph Traversal",
                "artist": "BFS/DFS",
                "album": "Data Structures",
                "duration_ms": 210000,
                "preview_url": None,
            },
            {
                "name": "Hash Function",
                "artist": "Constant Time",
                "album": "Performance Patterns",
                "duration_ms": 195000,
                "preview_url": "demo",
            },
        ],
    }

    return track_sets.get(playlist_id, track_sets["demo1"])


# API VIEWS FOR FRONTEND
def api_playlists(request):
    """API endpoint to get all playlists as JSON"""
    try:
        playlists = SpotifyPlaylist.objects.filter(is_public=True).order_by(
            "-updated_at"
        )

        playlist_data = []
        for playlist in playlists:
            playlist_data.append(
                {
                    "id": playlist.spotify_id,
                    "name": playlist.name,
                    "description": playlist.description or "",
                    "image_url": playlist.image_url,
                    "external_url": playlist.external_url,
                    "owner_name": playlist.owner_name,
                    "track_count": playlist.track_count,
                    "last_synced": (
                        playlist.last_synced.isoformat()
                        if playlist.last_synced
                        else None
                    ),
                }
            )

        return JsonResponse(
            {"success": True, "playlists": playlist_data, "total": len(playlist_data)}
        )

    except Exception as e:
        logger.error(f"API playlists error: {e}")
        return JsonResponse(
            {"success": False, "error": "Failed to fetch playlists"}, status=500
        )


def api_playlist_tracks(request, playlist_id):
    """API endpoint to get tracks for a specific playlist"""
    try:
        playlist = get_object_or_404(
            SpotifyPlaylist, spotify_id=playlist_id, is_public=True
        )
        tracks = playlist.tracks.all().order_by("track_number")

        track_data = []
        for track in tracks:
            # Format duration
            duration_minutes = track.duration_ms // 60000
            duration_seconds = (track.duration_ms % 60000) // 1000
            duration_formatted = f"{duration_minutes}:{duration_seconds:02d}"

            track_data.append(
                {
                    "id": track.spotify_id,
                    "name": track.name,
                    "artist": track.artist,
                    "album": track.album,
                    "duration_ms": track.duration_ms,
                    "duration_formatted": duration_formatted,
                    "preview_url": track.preview_url,
                    "external_url": track.external_url,
                    "track_number": track.track_number,
                }
            )

        return JsonResponse(
            {
                "success": True,
                "playlist": {
                    "id": playlist.spotify_id,
                    "name": playlist.name,
                    "description": playlist.description,
                    "image_url": playlist.image_url,
                    "track_count": playlist.track_count,
                },
                "tracks": track_data,
                "total_tracks": len(track_data),
            }
        )

    except SpotifyPlaylist.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Playlist not found"}, status=404
        )

    except Exception as e:
        logger.error(f"API playlist tracks error: {e}")
        return JsonResponse(
            {"success": False, "error": "Failed to fetch playlist tracks"}, status=500
        )
