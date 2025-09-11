import requests, base64
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

# Step 1: Redirect user to Spotify login
def spotify_login(request):
    scopes = "user-read-private user-read-email playlist-read-private playlist-read-collaborative"
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?response_type=code&client_id={settings.SPOTIFY_CLIENT_ID}"
        f"&scope={scopes}&redirect_uri={settings.SPOTIFY_REDIRECT_URI}"
    )
    logger.info(f"Redirecting to Spotify auth URL: {auth_url}")
    return redirect(auth_url)


# Step 2: Spotify redirects back with code → exchange for token
def spotify_callback(request):
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
        
        logger.info(f"Token exchange response status: {response.status_code}")
        
        if response.status_code == 200:
            tokens = response.json()
            request.session["spotify_access_token"] = tokens.get("access_token")
            request.session["spotify_refresh_token"] = tokens.get("refresh_token")
            
            logger.info("Successfully stored Spotify tokens in session")
            messages.success(request, "Successfully connected to Spotify!")
            return redirect("my_playlist")
        else:
            logger.error(f"Token exchange failed: {response.text}")
            messages.error(request, "Failed to exchange authorization code for access token")
            return redirect("my_playlist")
            
    except Exception as e:
        logger.error(f"Exception during token exchange: {str(e)}")
        messages.error(request, "An error occurred during Spotify authentication")
        return redirect("my_playlist")


# Step 3: Fetch playlists
def my_playlist(request):
    access_token = request.session.get("spotify_access_token")
    
    # If no access token, show demo content with option to connect Spotify
    if not access_token:
        logger.info("No Spotify access token found, showing demo content")
        demo_playlists = {
            'items': [
                {
                    'name': 'Coding Focus 🎯',
                    'owner': {'display_name': 'Roshan Damor'},
                    'images': [{'url': 'https://placehold.co/300x300/1a1a2e/16213e?text=Coding+Focus'}],
                    'external_urls': {'spotify': 'https://open.spotify.com/playlist/demo1'}
                },
                {
                    'name': 'Late Night Coding 🌙',
                    'owner': {'display_name': 'Roshan Damor'},
                    'images': [{'url': 'https://placehold.co/300x300/0f0f0f/ffd700?text=Late+Night'}],
                    'external_urls': {'spotify': 'https://open.spotify.com/playlist/demo2'}
                },
                {
                    'name': 'Debugging Chill 🐛',
                    'owner': {'display_name': 'Roshan Damor'},
                    'images': [{'url': 'https://placehold.co/300x300/2c3e50/e74c3c?text=Debug+Chill'}],
                    'external_urls': {'spotify': 'https://open.spotify.com/playlist/demo3'}
                },
                {
                    'name': 'Coffee & Code ☕',
                    'owner': {'display_name': 'Roshan Damor'},
                    'images': [{'url': 'https://placehold.co/300x300/8b4513/deb887?text=Coffee+Code'}],
                    'external_urls': {'spotify': 'https://open.spotify.com/playlist/demo4'}
                },
                {
                    'name': 'Productivity Beats 🚀',
                    'owner': {'display_name': 'Roshan Damor'},
                    'images': [{'url': 'https://placehold.co/300x300/4a90e2/ffffff?text=Productivity'}],
                    'external_urls': {'spotify': 'https://open.spotify.com/playlist/demo5'}
                },
                {
                    'name': 'Algorithm Vibes 🧮',
                    'owner': {'display_name': 'Roshan Damor'},
                    'images': [{'url': 'https://placehold.co/300x300/27ae60/ffffff?text=Algorithm'}],
                    'external_urls': {'spotify': 'https://open.spotify.com/playlist/demo6'}
                }
            ]
        }
        return render(request, "music/playlist.html", {
            "playlists": demo_playlists, 
            "is_demo": True,
            "spotify_login_url": "/music/spotify-login/"
        })

    # If authenticated, fetch real playlists
    logger.info("Access token found, attempting to fetch real Spotify playlists")
    try:
        url = "https://api.spotify.com/v1/me/playlists"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        logger.info(f"Making request to: {url}")
        response = requests.get(url, headers=headers)
        
        logger.info(f"Spotify API response status: {response.status_code}")
        
        if response.status_code == 200:
            playlists = response.json()
            logger.info(f"Successfully fetched {len(playlists.get('items', []))} playlists")
            
            # Add success message to show it's working
            if playlists.get('items'):
                messages.success(request, f"Successfully loaded {len(playlists['items'])} playlists from your Spotify account!")
            
            return render(request, "music/playlist.html", {"playlists": playlists, "is_demo": False})
        elif response.status_code == 401:
            # Token expired, clear session and redirect to login
            logger.warning("Spotify access token expired")
            request.session.pop("spotify_access_token", None)
            request.session.pop("spotify_refresh_token", None)
            messages.warning(request, "Your Spotify session has expired. Please reconnect.")
            return redirect("spotify_login")
        else:
            # Other error, show demo with error message
            logger.error(f"Spotify API error: {response.status_code} - {response.text}")
            return render(request, "music/playlist.html", {
                "playlists": {"items": []}, 
                "is_demo": True,
                "error_message": f"Unable to fetch playlists (Error {response.status_code}). Please try connecting again.",
                "spotify_login_url": "/music/spotify-login/"
            })
    except Exception as e:
        # Network error or other issues
        logger.error(f"Exception while fetching playlists: {str(e)}")
        return render(request, "music/playlist.html", {
            "playlists": {"items": []}, 
            "is_demo": True,
            "error_message": "Network error. Please check your connection and try again.",
            "spotify_login_url": "/music/spotify-login/"
        })


def playlist_tracks(request, playlist_id):
    access_token = request.session.get("spotify_access_token")
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    tracks = response.json()
    return JsonResponse(tracks)


def spotify_logout(request):
    """Logout from Spotify by clearing session data"""
    request.session.pop("spotify_access_token", None)
    request.session.pop("spotify_refresh_token", None)
    messages.info(request, "Disconnected from Spotify")
    return redirect("my_playlist")


def spotify_debug(request):
    """Debug view to check Spotify configuration"""
    debug_info = {
        'client_id': settings.SPOTIFY_CLIENT_ID[:10] + "..." if settings.SPOTIFY_CLIENT_ID else "Not set",
        'client_secret': "Set" if settings.SPOTIFY_CLIENT_SECRET else "Not set", 
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'session_token': "Present" if request.session.get("spotify_access_token") else "Not present",
        'full_client_id': settings.SPOTIFY_CLIENT_ID,  # For debugging - remove in production
        'current_host': request.get_host(),
        'is_secure': request.is_secure(),
        'protocol': 'https' if request.is_secure() else 'http',
    }
    
    # If we have a token, test it
    access_token = request.session.get("spotify_access_token")
    if access_token:
        try:
            url = "https://api.spotify.com/v1/me"
            response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
            debug_info['user_test'] = {
                'status': response.status_code,
                'response': response.json() if response.status_code == 200 else response.text
            }
        except Exception as e:
            debug_info['user_test'] = f"Error: {str(e)}"
    
    return JsonResponse(debug_info)


def spotify_test(request):
    """Test page for Spotify integration"""
    return render(request, "music/test.html")
