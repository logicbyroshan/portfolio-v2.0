import requests
import base64
import logging
import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import timedelta

from .models import (
    AboutMeConfiguration,
    ResourcesConfiguration,
    ResourceCategory,
    Resource,
    ResourceView,
    SpotifyPlaylist,
    SpotifyTrack,
    SpotifyToken,
    ManualPlaylist,
    ManualTrack,
)
from .forms import ResourceFilterForm, ManualPlaylistForm, ManualTrackForm

logger = logging.getLogger(__name__)


# =========================================================================
# ABOUT ME VIEW
# =========================================================================


class AboutMeView(TemplateView):
    """View for the About Me page."""

    template_name = "about-me.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            config = AboutMeConfiguration.objects.first()
            context["config"] = config
        except AboutMeConfiguration.DoesNotExist:
            context["config"] = None

        # Add FAQ data for the FAQ section
        from portfolio.models import FAQ

        context["faqs"] = FAQ.objects.order_by("order")

        return context


# =========================================================================
# RESOURCES VIEWS
# =========================================================================


class ResourcesListView(ListView):
    """View for the resources list page with filtering and pagination."""

    model = Resource
    template_name = "resources-list.html"
    context_object_name = "resources"
    paginate_by = 12

    def get_queryset(self):
        queryset = Resource.objects.filter(is_active=True)

        # Get filter parameters from form
        category_slug = self.request.GET.get("category")
        resource_type = self.request.GET.get("type")
        search_query = self.request.GET.get("search")
        sort_by = self.request.GET.get("sort", "newest")

        # Apply filters
        if category_slug and category_slug != "all":
            queryset = queryset.filter(categories__slug=category_slug)

        if resource_type and resource_type != "all":
            queryset = queryset.filter(resource_type=resource_type)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(author__icontains=search_query)
            )

        # Apply sorting
        if sort_by == "oldest":
            queryset = queryset.order_by("created_date")
        elif sort_by == "rating":
            queryset = queryset.order_by("-personal_rating", "-created_date")
        elif sort_by == "title":
            queryset = queryset.order_by("title")
        else:  # newest
            queryset = queryset.order_by("-created_date")

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add configuration
        try:
            resources_config = ResourcesConfiguration.objects.first()
            context["resources_config"] = resources_config
        except ResourcesConfiguration.DoesNotExist:
            context["resources_config"] = None

        # Add filter form and related data
        context["form"] = ResourceFilterForm(self.request.GET)
        context["categories"] = ResourceCategory.objects.all().order_by("order", "name")
        context["resource_types"] = Resource.ResourceType.choices

        # Add current filter values
        context["current_category"] = self.request.GET.get("category", "all")
        context["current_type"] = self.request.GET.get("type", "all")
        context["current_search"] = self.request.GET.get("search", "")
        context["current_sort"] = self.request.GET.get("sort", "newest")

        return context


class ResourceDetailView(DetailView):
    """View for individual resource detail pages."""

    model = Resource
    template_name = "resource-detail.html"
    context_object_name = "resource"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Resource.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = self.get_object()

        # Get related resources
        context["related_resources"] = self._get_related_resources(resource)

        return context

    def get(self, request, *args, **kwargs):
        # Record view
        resource = self.get_object()
        ResourceView.objects.create(
            resource=resource,
            ip_address=self._get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        )
        return super().get(request, *args, **kwargs)

    def _get_related_resources(self, resource):
        """Get related resources based on categories and technologies."""
        try:
            # Get resources with similar categories or technologies
            related = (
                Resource.objects.filter(
                    Q(categories__in=resource.categories.all())
                    | Q(technologies__in=resource.technologies.all()),
                    is_active=True,
                )
                .exclude(pk=resource.pk)
                .distinct()[:4]
            )

            return related
        except Exception:
            return Resource.objects.none()

    def _get_client_ip(self, request):
        """Get client IP address from request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


# =========================================================================
# MUSIC/PLAYLIST VIEWS
# =========================================================================


def is_admin(user):
    """Check if user is admin/staff"""
    return user.is_staff or user.is_superuser


def my_playlist(request):
    """Public view showing both Spotify and manual playlists"""
    # Get all public playlists from database
    spotify_playlists = SpotifyPlaylist.objects.filter(is_public=True)
    manual_playlists = ManualPlaylist.objects.filter(is_public=True)

    # Convert to unified format for template compatibility
    combined_playlists = []

    # Add Spotify playlists
    for playlist in spotify_playlists:
        combined_playlists.append(
            {
                "id": playlist.spotify_id,
                "name": playlist.name,
                "description": playlist.description or "",
                "owner": {"display_name": playlist.owner_name},
                "images": [{"url": playlist.image_url}] if playlist.image_url else [],
                "external_urls": {"spotify": playlist.external_url},
                "tracks": {"total": playlist.track_count},
                "last_synced": playlist.last_synced,
                "type": "spotify",
                "playlist_obj": playlist,
            }
        )

    # Add manual playlists
    for playlist in manual_playlists:
        image_url = (
            playlist.cover_image.url
            if playlist.cover_image
            else "https://placehold.co/300x300/010409/00A9FF?text=" + playlist.name[:1]
        )
        combined_playlists.append(
            {
                "id": f"manual_{playlist.id}",
                "name": playlist.name,
                "description": playlist.description or "",
                "owner": {"display_name": "Roshan Damor"},
                "images": [{"url": image_url}],
                "external_urls": {"spotify": "#"},
                "tracks": {"total": playlist.track_count},
                "last_synced": None,
                "type": "manual",
                "playlist_obj": playlist,
            }
        )

    # Sort by type (manual first) and then by name
    combined_playlists.sort(key=lambda x: (x["type"] == "spotify", x["name"]))

    playlist_data = {"items": combined_playlists}

    # Check if we have any playlists
    if not combined_playlists:
        # Show demo playlists if no real data with sample audio
        demo_playlists = {
            "items": [
                {
                    "id": "demo1",
                    "name": "Coding Focus 🎯",
                    "description": "Perfect beats for deep focus and productive coding sessions",
                    "owner": {"display_name": "Roshan Damor"},
                    "images": [
                        {
                            "url": "https://i.scdn.co/image/ab67616d0000b273a7e2150e8a2d9b1b5e5c8b4f"
                        }
                    ],
                    "external_urls": {"spotify": "#"},
                    "tracks": {"total": 42},
                    "last_synced": timezone.now(),
                    "demo_tracks": [
                        {
                            "name": "Lo-Fi Dreams",
                            "artist": "ChillBeats",
                            "duration": "3:24",
                        },
                        {
                            "name": "Coffee Shop Vibes",
                            "artist": "StudyMusic",
                            "duration": "4:12",
                        },
                        {
                            "name": "Midnight Code",
                            "artist": "DevBeats",
                            "duration": "3:56",
                        },
                    ],
                },
                {
                    "id": "demo2",
                    "name": "Workout Energy ⚡",
                    "description": "High-energy tracks to fuel your workout sessions",
                    "owner": {"display_name": "Roshan Damor"},
                    "images": [
                        {
                            "url": "https://i.scdn.co/image/ab67616d0000b273b5e5c8b4f7a2e21509d1b1b5"
                        }
                    ],
                    "external_urls": {"spotify": "#"},
                    "tracks": {"total": 28},
                    "last_synced": timezone.now(),
                    "demo_tracks": [
                        {
                            "name": "Thunder Strike",
                            "artist": "PowerBeats",
                            "duration": "3:45",
                        },
                        {
                            "name": "Electric Rush",
                            "artist": "GymHits",
                            "duration": "4:20",
                        },
                        {
                            "name": "Victory Anthem",
                            "artist": "MotivationFM",
                            "duration": "3:33",
                        },
                    ],
                },
                {
                    "id": "demo3",
                    "name": "Chill Evenings 🌙",
                    "description": "Relaxing tunes for unwinding after a long day",
                    "owner": {"display_name": "Roshan Damor"},
                    "images": [
                        {
                            "url": "https://i.scdn.co/image/ab67616d0000b273c8b4f7a2e21509d1b1b5e5c8"
                        }
                    ],
                    "external_urls": {"spotify": "#"},
                    "tracks": {"total": 35},
                    "last_synced": timezone.now(),
                    "demo_tracks": [
                        {
                            "name": "Sunset Dreams",
                            "artist": "ChillVibes",
                            "duration": "4:18",
                        },
                        {
                            "name": "Ocean Breeze",
                            "artist": "RelaxTunes",
                            "duration": "5:02",
                        },
                        {
                            "name": "Moonlight Serenade",
                            "artist": "EveningJazz",
                            "duration": "4:45",
                        },
                    ],
                },
            ]
        }
        playlist_data = demo_playlists

    return render(
        request,
        "music/playlist.html",
        {"playlists": playlist_data, "is_demo": not combined_playlists},
    )


def playlist_detail(request, playlist_id):
    """Show detailed view of a specific playlist with tracks"""
    playlist = None
    tracks = []
    tracks_data = []

    # Check if it's a manual playlist
    if playlist_id.startswith("manual_"):
        manual_id = playlist_id.replace("manual_", "")
        try:
            playlist = ManualPlaylist.objects.get(id=manual_id)
            tracks = playlist.manual_tracks.filter(is_active=True)

            # Prepare tracks data for JavaScript
            for track in tracks:
                audio_source = track.primary_audio_source
                tracks_data.append(
                    {
                        "id": f"manual_{track.id}",
                        "name": track.name,
                        "artist": track.artist,
                        "album": track.album,
                        "preview_url": audio_source["url"] if audio_source else None,
                        "audio_type": audio_source["type"] if audio_source else None,
                        "external_url": track.spotify_url or track.youtube_url or "#",
                        "duration_ms": track.duration_ms,
                        "track_number": track.track_number,
                        "youtube_url": track.youtube_url,
                        "spotify_url": track.spotify_url,
                        "apple_music_url": track.apple_music_url,
                    }
                )
        except ManualPlaylist.DoesNotExist:
            messages.error(request, "Playlist not found.")
            return redirect("roshan:my_playlist")
    else:
        # It's a Spotify playlist
        try:
            playlist = SpotifyPlaylist.objects.get(spotify_id=playlist_id)
            tracks = playlist.tracks.all()

            # Prepare tracks data for JavaScript
            for track in tracks:
                tracks_data.append(
                    {
                        "id": track.spotify_id,
                        "name": track.name,
                        "artist": track.artist,
                        "album": track.album,
                        "preview_url": track.preview_url,
                        "audio_type": "spotify",
                        "external_url": track.external_url,
                        "duration_ms": track.duration_ms,
                        "track_number": track.track_number,
                    }
                )
        except SpotifyPlaylist.DoesNotExist:
            messages.error(request, "Playlist not found.")
            return redirect("roshan:my_playlist")

    return render(
        request,
        "music/playlist_detail.html",
        {
            "playlist": playlist,
            "tracks": tracks,
            "tracks_json": json.dumps(tracks_data),
            "is_manual": playlist_id.startswith("manual_"),
        },
    )


# =========================================================================
# MANUAL PLAYLIST VIEWS
# =========================================================================


@login_required
@user_passes_test(lambda u: u.is_staff)
def create_manual_playlist(request):
    """Create a new manual playlist"""
    if request.method == "POST":
        form = ManualPlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save()
            messages.success(
                request, f'Playlist "{playlist.name}" created successfully!'
            )
            return JsonResponse(
                {
                    "success": True,
                    "playlist_id": playlist.id,
                    "redirect_url": f"/playlist/manual_{playlist.id}/",
                }
            )
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = ManualPlaylistForm()

    return render(request, "music/create_playlist_modal.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def add_track_to_playlist(request, playlist_id):
    """Add a track to a manual playlist"""
    try:
        playlist = ManualPlaylist.objects.get(id=playlist_id)
    except ManualPlaylist.DoesNotExist:
        return JsonResponse({"success": False, "error": "Playlist not found"})

    if request.method == "POST":
        form = ManualTrackForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            track.playlist = playlist

            # Set track number if not provided
            if not track.track_number:
                last_track = playlist.manual_tracks.order_by("-track_number").first()
                track.track_number = (last_track.track_number + 1) if last_track else 1

            track.save()
            messages.success(request, f'Track "{track.name}" added to playlist!')
            return JsonResponse(
                {"success": True, "track_id": track.id, "track_name": track.name}
            )
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = ManualTrackForm()

    return render(
        request, "music/add_track_modal.html", {"form": form, "playlist": playlist}
    )


@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_manual_playlist(request, playlist_id):
    """Edit a manual playlist"""
    try:
        playlist = ManualPlaylist.objects.get(id=playlist_id)
    except ManualPlaylist.DoesNotExist:
        messages.error(request, "Playlist not found.")
        return redirect("roshan:my_playlist")

    if request.method == "POST":
        form = ManualPlaylistForm(request.POST, request.FILES, instance=playlist)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Playlist "{playlist.name}" updated successfully!'
            )
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = ManualPlaylistForm(instance=playlist)

    return render(
        request, "music/edit_playlist_modal.html", {"form": form, "playlist": playlist}
    )


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_manual_playlist(request, playlist_id):
    """Delete a manual playlist"""
    if request.method == "POST":
        try:
            playlist = ManualPlaylist.objects.get(id=playlist_id)
            playlist_name = playlist.name
            playlist.delete()
            messages.success(
                request, f'Playlist "{playlist_name}" deleted successfully!'
            )
            return JsonResponse({"success": True})
        except ManualPlaylist.DoesNotExist:
            return JsonResponse({"success": False, "error": "Playlist not found"})

    return JsonResponse({"success": False, "error": "Invalid request method"})


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_manual_track(request, track_id):
    """Delete a track from a manual playlist"""
    if request.method == "POST":
        try:
            track = ManualTrack.objects.get(id=track_id)
            track_name = track.name
            track.delete()
            messages.success(request, f'Track "{track_name}" removed from playlist!')
            return JsonResponse({"success": True})
        except ManualTrack.DoesNotExist:
            return JsonResponse({"success": False, "error": "Track not found"})

    return JsonResponse({"success": False, "error": "Invalid request method"})


# =========================================================================
# ADMIN SPOTIFY VIEWS
# =========================================================================


@login_required
@user_passes_test(is_admin)
def admin_spotify_config(request):
    """Admin view for Spotify API configuration"""
    current_token = SpotifyToken.objects.first()

    # Check if we have required settings
    missing_settings = []
    if not getattr(settings, "SPOTIFY_CLIENT_ID", None):
        missing_settings.append("SPOTIFY_CLIENT_ID")
    if not getattr(settings, "SPOTIFY_CLIENT_SECRET", None):
        missing_settings.append("SPOTIFY_CLIENT_SECRET")
    if not getattr(settings, "SPOTIFY_REDIRECT_URI", None):
        missing_settings.append("SPOTIFY_REDIRECT_URI")

    context = {
        "current_token": current_token,
        "missing_settings": missing_settings,
        "auth_url": None,
    }

    if not missing_settings:
        # Generate Spotify auth URL
        auth_url = (
            "https://accounts.spotify.com/authorize?"
            f"client_id={settings.SPOTIFY_CLIENT_ID}&"
            f"response_type=code&"
            f"redirect_uri={settings.SPOTIFY_REDIRECT_URI}&"
            f"scope=playlist-read-private playlist-read-collaborative"
        )
        context["auth_url"] = auth_url

    return render(request, "music/admin_config.html", context)


def admin_spotify_callback(request):
    """Handle Spotify OAuth callback"""
    code = request.GET.get("code")
    error = request.GET.get("error")

    if error:
        messages.error(request, f"Spotify authorization failed: {error}")
        return redirect("roshan:admin_spotify_config")

    if not code:
        messages.error(request, "No authorization code received")
        return redirect("roshan:admin_spotify_config")

    try:
        # Exchange code for tokens
        token_data = exchange_code_for_tokens(code)

        # Store tokens
        SpotifyToken.objects.all().delete()  # Remove old tokens
        SpotifyToken.objects.create(
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            expires_at=timezone.now() + timedelta(seconds=token_data["expires_in"]),
        )

        messages.success(
            request, "Spotify authorization successful! You can now sync playlists."
        )

    except Exception as e:
        logger.error(f"Error during Spotify callback: {e}")
        messages.error(request, f"Error during authorization: {str(e)}")

    return redirect("roshan:admin_spotify_config")


@login_required
@user_passes_test(is_admin)
def sync_playlists(request):
    """Sync playlists from Spotify API"""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Method not allowed"})

    try:
        token = get_valid_token()
        if not token:
            return JsonResponse(
                {"success": False, "error": "No valid Spotify token available"}
            )

        # Fetch playlists from Spotify
        playlists_data = fetch_spotify_playlists(token.access_token)

        if not playlists_data:
            return JsonResponse(
                {"success": False, "error": "Failed to fetch playlists from Spotify"}
            )

        synced_count = 0
        for playlist_data in playlists_data.get("items", []):
            playlist, created = sync_single_playlist(playlist_data, token.access_token)
            if playlist:
                synced_count += 1

        return JsonResponse(
            {
                "success": True,
                "message": f"Successfully synced {synced_count} playlists",
                "synced_count": synced_count,
            }
        )

    except Exception as e:
        logger.error(f"Error syncing playlists: {e}")
        return JsonResponse({"success": False, "error": str(e)})


# =========================================================================
# SPOTIFY API HELPER FUNCTIONS
# =========================================================================


def exchange_code_for_tokens(code):
    """Exchange authorization code for access and refresh tokens"""
    token_url = "https://accounts.spotify.com/api/token"

    # Prepare request
    auth_string = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
    }

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()

    return response.json()


def get_valid_token():
    """Get a valid access token, refreshing if necessary"""
    token = SpotifyToken.objects.first()
    if not token:
        return None

    # Check if token is expired
    if timezone.now() >= token.expires_at:
        # Try to refresh
        try:
            new_token_data = refresh_access_token(token.refresh_token)
            token.access_token = new_token_data["access_token"]
            token.expires_at = timezone.now() + timedelta(
                seconds=new_token_data["expires_in"]
            )

            # Update refresh token if provided
            if "refresh_token" in new_token_data:
                token.refresh_token = new_token_data["refresh_token"]

            token.save()

        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return None

    return token


def refresh_access_token(refresh_token):
    """Refresh the access token using refresh token"""
    token_url = "https://accounts.spotify.com/api/token"

    # Prepare request
    auth_string = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()

    return response.json()


def fetch_spotify_playlists(access_token):
    """Fetch user's playlists from Spotify API"""
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def sync_single_playlist(playlist_data, access_token):
    """Sync a single playlist and its tracks"""
    try:
        # Create or update playlist
        playlist, created = SpotifyPlaylist.objects.update_or_create(
            spotify_id=playlist_data["id"],
            defaults={
                "name": playlist_data["name"],
                "description": playlist_data.get("description", ""),
                "image_url": (
                    playlist_data["images"][0]["url"]
                    if playlist_data.get("images")
                    else None
                ),
                "external_url": playlist_data["external_urls"]["spotify"],
                "owner_name": playlist_data["owner"]["display_name"],
                "track_count": playlist_data["tracks"]["total"],
                "is_public": playlist_data.get("public", True),
                "last_synced": timezone.now(),
            },
        )

        # Fetch and sync tracks
        tracks_data = fetch_playlist_tracks(playlist_data["id"], access_token)
        if tracks_data:
            sync_playlist_tracks(playlist, tracks_data)

        return playlist, created

    except Exception as e:
        logger.error(
            f"Error syncing playlist {playlist_data.get('id', 'unknown')}: {e}"
        )
        return None, False


def fetch_playlist_tracks(playlist_id, access_token):
    """Fetch tracks for a specific playlist"""
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def sync_playlist_tracks(playlist, tracks_data):
    """Sync tracks for a playlist"""
    # Clear existing tracks
    playlist.tracks.all().delete()

    # Add new tracks
    for i, item in enumerate(tracks_data.get("items", [])):
        track_data = item.get("track")
        if not track_data:
            continue

        SpotifyTrack.objects.create(
            playlist=playlist,
            spotify_id=track_data["id"],
            name=track_data["name"],
            artist=", ".join([artist["name"] for artist in track_data["artists"]]),
            album=track_data["album"]["name"],
            duration_ms=track_data["duration_ms"],
            preview_url=track_data.get("preview_url"),
            external_url=track_data["external_urls"]["spotify"],
            track_number=i + 1,
        )


# =========================================================================
# LEGAL PAGES VIEWS
# =========================================================================


class PrivacyPolicyView(TemplateView):
    """View for the Privacy Policy page."""

    template_name = "legal/privacy-policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Privacy Policy"
        context["last_updated"] = "October 2025"
        return context


class TermsOfServiceView(TemplateView):
    """View for the Terms of Service page."""

    template_name = "legal/terms-of-service.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Terms of Service"
        context["last_updated"] = "October 2025"
        return context
