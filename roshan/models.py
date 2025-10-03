from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from tinymce.models import HTMLField
import bleach

ALLOWED_TAGS = ["b", "i", "strong", "em", "u", "a", "br", "p", "ul", "ol", "li", "span"]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
    "span": ["style"],
}


def sanitize_html(value):
    if value:
        return bleach.clean(
            value, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True
        )
    return value


# =========================================================================
# ABOUT ME PAGE CONFIGURATION MODEL
# =========================================================================


class AboutMeConfiguration(models.Model):
    # --- Page Header ---
    page_title = models.CharField(
        max_length=255, default="A Bit More <span>About Me</span>"
    )
    intro_paragraph = models.TextField(
        default="This is my story, my journey, and what drives me."
    )
    profile_image = models.ImageField(
        upload_to="about/",
        blank=True,
        null=True,
        help_text="Profile image for About Me page",
    )
    detailed_description = HTMLField(
        default="""<ul>
            <li><strong>Mission:</strong> To build software that is not only functional but also intuitive and impactful.</li>
            <li><strong>Interests:</strong> Beyond coding, I'm passionate about AI ethics, open-source contribution, and exploring the intersection of technology and art.</li>
        </ul>""",
        help_text="Detailed description with HTML support",
    )

    # --- Meta Information ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Me Configuration"
        verbose_name_plural = "About Me Configuration"

    def __str__(self):
        return "About Me Page Configuration"

    def save(self, *args, **kwargs):
        """Ensure only one instance exists."""
        if not self.pk and AboutMeConfiguration.objects.exists():
            # Update existing instance instead of creating new one
            existing = AboutMeConfiguration.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)


# =========================================================================
# RESOURCES PAGE MODELS
# =========================================================================


class ResourcesConfiguration(models.Model):
    # --- Page Header ---
    page_title = HTMLField(default="My Curated <span>Resources</span>")
    intro_paragraph = models.TextField(
        max_length=500,
    )
    resources_description = HTMLField(
        help_text="Additional description content for the resources section", blank=True
    )
    resources_per_page = models.PositiveIntegerField(
        default=12, help_text="Number of resources to display per page"
    )

    # --- Meta Information ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Resources Configuration"
        verbose_name_plural = "Resources Configuration"

    def __str__(self):
        return "Resources Page Configuration"

    def save(self, *args, **kwargs):
        """Ensure only one instance exists."""
        if not self.pk and ResourcesConfiguration.objects.exists():
            # Update existing instance instead of creating new one
            existing = ResourcesConfiguration.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)


class ResourceCategory(models.Model):
    """
    Model for categorizing resources (separate from general categories).
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    description = HTMLField(
        max_length=200,
        blank=True,
        help_text="Brief description of this resource category with HTML support",
    )
    icon = models.CharField(
        max_length=50,
        default="fa-solid fa-folder",
        help_text="Font Awesome icon class (e.g., 'fa-solid fa-code')",
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Display order for category filtering"
    )

    class Meta:
        verbose_name_plural = "Resource Categories"
        ordering = ["order", "name"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description = sanitize_html(self.description)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Resource(models.Model):
    # --- Resource Type Choices ---
    class ResourceType(models.TextChoices):
        ARTICLE = "ART", "Article"
        VIDEO = "VID", "Video"
        PDF = "PDF", "PDF Document"
        TOOL = "TOL", "Tool/Website"
        COURSE = "CRS", "Course"
        BOOK = "BOK", "Book"
        TUTORIAL = "TUT", "Tutorial"
        DOCUMENTATION = "DOC", "Documentation"
        REPOSITORY = "REP", "Code Repository"
        OTHER = "OTH", "Other"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    description = HTMLField(
        max_length=300, help_text="Brief description of the resource with HTML support"
    )
    resource_type = models.CharField(
        max_length=3, choices=ResourceType.choices, default=ResourceType.ARTICLE
    )
    link = models.URLField(
        blank=True, null=True, help_text="External link to the resource"
    )
    file_upload = models.FileField(
        upload_to="resources/files/",
        blank=True,
        null=True,
        help_text="Upload file for downloadable resources (PDFs, documents, etc.)",
    )
    youtube_embed_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="YouTube video ID for embedding (e.g., 'dQw4w9WgXcQ')",
    )
    vimeo_embed_id = models.CharField(
        max_length=50, blank=True, help_text="Vimeo video ID for embedding"
    )
    custom_embed_code = HTMLField(
        blank=True, help_text="Custom embed code for other video platforms or widgets"
    )
    thumbnail = models.ImageField(
        upload_to="resources/thumbnails/",
        blank=True,
        null=True,
        help_text="Thumbnail image for the resource",
    )
    preview_image = models.ImageField(
        upload_to="resources/previews/",
        blank=True,
        null=True,
        help_text="Preview image for PDFs or other documents",
    )
    categories = models.ManyToManyField(
        ResourceCategory, related_name="resources", blank=True
    )
    technologies = models.ManyToManyField(
        "portfolio.Technology",
        related_name="resources",
        blank=True,
        help_text="Related technologies or tech stack",
    )
    author = models.CharField(
        max_length=100,
        blank=True,
        help_text="Original author or creator of the resource",
    )
    publication_date = models.DateField(
        blank=True, null=True, help_text="When the resource was originally published"
    )
    is_featured = models.BooleanField(
        default=False, help_text="Display this resource prominently"
    )
    is_active = models.BooleanField(
        default=True, help_text="Whether this resource should be displayed"
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Display order within category"
    )
    personal_rating = models.PositiveIntegerField(
        default=5,
        choices=[(i, f"{i} Stars") for i in range(1, 6)],
        help_text="Your personal rating of this resource (1-5 stars)",
    )

    # --- Timestamps ---
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_date"]
        verbose_name = "Resource"
        verbose_name_plural = "Resources"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.description = sanitize_html(self.description)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_resource_type_display()})"

    @property
    def has_video_embed(self):
        """Check if resource has any video embed information."""
        return bool(
            self.youtube_embed_id or self.vimeo_embed_id or self.custom_embed_code
        )

    @property
    def embed_url(self):
        """Get the appropriate embed URL based on platform."""
        if self.youtube_embed_id:
            return f"https://www.youtube.com/embed/{self.youtube_embed_id}"
        elif self.vimeo_embed_id:
            return f"https://player.vimeo.com/video/{self.vimeo_embed_id}"
        return None

    @property
    def is_downloadable(self):
        """Check if resource has downloadable content."""
        return bool(self.file_upload)

    @property
    def display_thumbnail(self):
        """Get appropriate thumbnail - uploaded thumbnail, preview image, or default based on type."""
        if self.thumbnail:
            return self.thumbnail.url
        elif self.preview_image:
            return self.preview_image.url
        elif self.youtube_embed_id:
            return (
                f"https://img.youtube.com/vi/{self.youtube_embed_id}/maxresdefault.jpg"
            )
        return None


class ResourceView(models.Model):
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="views"
    )
    viewed_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        verbose_name = "Resource View"
        verbose_name_plural = "Resource Views"

    def __str__(self):
        return f"View of {self.resource.title} on {self.viewed_date.date()}"


# =========================================================================
# SPOTIFY/MUSIC MODELS (from music app)
# =========================================================================


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
        ordering = ["-updated_at"]
        verbose_name = "Spotify Playlist"
        verbose_name_plural = "Spotify Playlists"

    def __str__(self):
        return self.name


class SpotifyTrack(models.Model):
    playlist = models.ForeignKey(
        SpotifyPlaylist, related_name="tracks", on_delete=models.CASCADE
    )
    spotify_id = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, blank=True)
    duration_ms = models.IntegerField(default=0)
    preview_url = models.URLField(blank=True, null=True)
    external_url = models.URLField()
    track_number = models.IntegerField(default=0)

    class Meta:
        ordering = ["track_number"]
        unique_together = ["playlist", "spotify_id"]
        verbose_name = "Spotify Track"
        verbose_name_plural = "Spotify Tracks"

    def __str__(self):
        return f"{self.name} by {self.artist}"

    @property
    def duration_formatted(self):
        """Format duration from milliseconds to MM:SS"""
        if not self.duration_ms:
            return "0:00"

        total_seconds = self.duration_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"


class SpotifyToken(models.Model):
    """Store admin's Spotify tokens for periodic sync"""

    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Spotify Token"
        verbose_name_plural = "Spotify Tokens"

    def __str__(self):
        return f"Spotify Token (expires: {self.expires_at})"


# =========================================================================
# MANUAL PLAYLIST MODELS
# =========================================================================


class ManualPlaylist(models.Model):
    """Manually created playlists with custom tracks"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(
        upload_to="playlists/covers/",
        blank=True,
        null=True,
        help_text="Cover image for the playlist",
    )
    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Manual Playlist"
        verbose_name_plural = "Manual Playlists"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def track_count(self):
        return self.manual_tracks.count()

    @property
    def total_duration(self):
        """Calculate total duration of all tracks"""
        total_ms = sum(
            track.duration_ms for track in self.manual_tracks.all() if track.duration_ms
        )
        if not total_ms:
            return "0:00"

        total_seconds = total_ms // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:00"
        return f"{minutes}:00"


class ManualTrack(models.Model):
    """Individual tracks in manual playlists"""

    playlist = models.ForeignKey(
        ManualPlaylist, related_name="manual_tracks", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, blank=True)
    duration_ms = models.IntegerField(default=0, help_text="Duration in milliseconds")
    audio_file = models.FileField(
        upload_to="playlists/tracks/",
        blank=True,
        null=True,
        help_text="Upload audio file (MP3, WAV, etc.)",
    )
    youtube_url = models.URLField(
        blank=True, null=True, help_text="YouTube URL for the track"
    )
    spotify_url = models.URLField(
        blank=True, null=True, help_text="Spotify URL for the track"
    )
    apple_music_url = models.URLField(
        blank=True, null=True, help_text="Apple Music URL for the track"
    )
    track_number = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["track_number", "created_at"]
        verbose_name = "Manual Track"
        verbose_name_plural = "Manual Tracks"

    def __str__(self):
        return f"{self.name} by {self.artist}"

    @property
    def duration_formatted(self):
        """Format duration from milliseconds to MM:SS"""
        if not self.duration_ms:
            return "0:00"

        total_seconds = self.duration_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"

    @property
    def has_audio_source(self):
        """Check if track has any playable audio source"""
        return bool(self.audio_file or self.youtube_url)

    @property
    def primary_audio_source(self):
        """Get the primary audio source for playback"""
        if self.audio_file:
            return {"type": "file", "url": self.audio_file.url}
        elif self.youtube_url:
            return {"type": "youtube", "url": self.youtube_url}
        return None
