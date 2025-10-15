# Generated manually for roshan app

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AboutMeConfiguration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "page_title",
                    models.CharField(
                        default="A Bit More <span>About Me</span>", max_length=255
                    ),
                ),
                (
                    "intro_paragraph",
                    models.TextField(
                        default="This is my story, my journey, and what drives me."
                    ),
                ),
                (
                    "profile_image",
                    models.ImageField(
                        blank=True,
                        help_text="Profile image for About Me page",
                        null=True,
                        upload_to="about/",
                    ),
                ),
                (
                    "detailed_description",
                    tinymce.models.HTMLField(
                        default="<ul>\n            <li><strong>Mission:</strong> To build software that is not only functional but also intuitive and impactful.</li>\n            <li><strong>Interests:</strong> Beyond coding, I'm passionate about AI ethics, open-source contribution, and exploring the intersection of technology and art.</li>\n        </ul>",
                        help_text="Detailed description with HTML support",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "About Me Configuration",
                "verbose_name_plural": "About Me Configuration",
            },
        ),
        migrations.CreateModel(
            name="ResourceCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(editable=False, max_length=100, unique=True)),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Brief description of this resource category with HTML support",
                        max_length=200,
                    ),
                ),
                (
                    "icon",
                    models.CharField(
                        default="fa-solid fa-folder",
                        help_text="Font Awesome icon class (e.g., 'fa-solid fa-code')",
                        max_length=50,
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(
                        default=0, help_text="Display order for category filtering"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Resource Categories",
                "ordering": ["order", "name"],
            },
        ),
        migrations.CreateModel(
            name="ResourcesConfiguration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "page_title",
                    tinymce.models.HTMLField(
                        default="My Curated <span>Resources</span>"
                    ),
                ),
                ("intro_paragraph", models.TextField(max_length=500)),
                (
                    "resources_description",
                    tinymce.models.HTMLField(
                        blank=True,
                        help_text="Additional description content for the resources section",
                    ),
                ),
                (
                    "resources_per_page",
                    models.PositiveIntegerField(
                        default=12, help_text="Number of resources to display per page"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Resources Configuration",
                "verbose_name_plural": "Resources Configuration",
            },
        ),
        migrations.CreateModel(
            name="SpotifyPlaylist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("spotify_id", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("image_url", models.URLField(blank=True, null=True)),
                ("external_url", models.URLField()),
                ("owner_name", models.CharField(max_length=100)),
                ("track_count", models.PositiveIntegerField(default=0)),
                ("is_public", models.BooleanField(default=True)),
                ("last_synced", models.DateTimeField(auto_now=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Spotify Playlist",
                "verbose_name_plural": "Spotify Playlists",
                "ordering": ["-last_synced"],
            },
        ),
        migrations.CreateModel(
            name="SpotifyToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("access_token", models.TextField()),
                ("refresh_token", models.TextField()),
                ("expires_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Spotify Token",
                "verbose_name_plural": "Spotify Tokens",
            },
        ),
        migrations.CreateModel(
            name="SpotifyTrack",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("spotify_id", models.CharField(max_length=100)),
                ("name", models.CharField(max_length=255)),
                ("artist", models.CharField(max_length=255)),
                ("album", models.CharField(max_length=255)),
                ("duration_ms", models.PositiveIntegerField()),
                ("preview_url", models.URLField(blank=True, null=True)),
                ("external_url", models.URLField()),
                ("track_number", models.PositiveIntegerField(default=1)),
                (
                    "playlist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tracks",
                        to="roshan.spotifyplaylist",
                    ),
                ),
            ],
            options={
                "verbose_name": "Spotify Track",
                "verbose_name_plural": "Spotify Tracks",
                "ordering": ["track_number"],
            },
        ),
        migrations.CreateModel(
            name="Resource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(editable=False, max_length=200, unique=True)),
                (
                    "description",
                    tinymce.models.HTMLField(
                        help_text="Brief description of the resource with HTML support"
                    ),
                ),
                (
                    "resource_type",
                    models.CharField(
                        choices=[
                            ("ART", "Article"),
                            ("VID", "Video"),
                            ("PDF", "PDF Document"),
                            ("TOL", "Tool/Website"),
                            ("CRS", "Course"),
                            ("BOK", "Book"),
                            ("TUT", "Tutorial"),
                            ("DOC", "Documentation"),
                            ("REP", "Code Repository"),
                            ("OTH", "Other"),
                        ],
                        default="ART",
                        max_length=3,
                    ),
                ),
                (
                    "link",
                    models.URLField(
                        blank=True, help_text="External link to the resource", null=True
                    ),
                ),
                (
                    "file_upload",
                    models.FileField(
                        blank=True,
                        help_text="Upload file for downloadable resources (PDFs, documents, etc.)",
                        null=True,
                        upload_to="resources/files/",
                    ),
                ),
                (
                    "youtube_embed_id",
                    models.CharField(
                        blank=True,
                        help_text="YouTube video ID for embedding (e.g., 'dQw4w9WgXcQ')",
                        max_length=50,
                    ),
                ),
                (
                    "vimeo_embed_id",
                    models.CharField(
                        blank=True,
                        help_text="Vimeo video ID for embedding",
                        max_length=50,
                    ),
                ),
                (
                    "custom_embed_code",
                    tinymce.models.HTMLField(
                        blank=True,
                        help_text="Custom embed code for other video platforms or widgets",
                    ),
                ),
                (
                    "thumbnail",
                    models.ImageField(
                        blank=True,
                        help_text="Thumbnail image for the resource",
                        null=True,
                        upload_to="resources/thumbnails/",
                    ),
                ),
                (
                    "preview_image",
                    models.ImageField(
                        blank=True,
                        help_text="Preview image for PDFs or other documents",
                        null=True,
                        upload_to="resources/previews/",
                    ),
                ),
                (
                    "author",
                    models.CharField(
                        blank=True,
                        help_text="Original author or creator of the resource",
                        max_length=100,
                    ),
                ),
                (
                    "publication_date",
                    models.DateField(
                        blank=True,
                        help_text="When the resource was originally published",
                        null=True,
                    ),
                ),
                (
                    "is_featured",
                    models.BooleanField(
                        default=False, help_text="Display this resource prominently"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Whether this resource should be displayed",
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(
                        default=0, help_text="Display order within category"
                    ),
                ),
                (
                    "personal_rating",
                    models.PositiveIntegerField(
                        choices=[
                            (1, "1 Stars"),
                            (2, "2 Stars"),
                            (3, "3 Stars"),
                            (4, "4 Stars"),
                            (5, "5 Stars"),
                        ],
                        default=5,
                        help_text="Your personal rating of this resource (1-5 stars)",
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                (
                    "categories",
                    models.ManyToManyField(
                        blank=True,
                        related_name="resources",
                        to="roshan.resourcecategory",
                    ),
                ),
                (
                    "technologies",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Related technologies or tech stack",
                        related_name="resources",
                        to="portfolio.technology",
                    ),
                ),
            ],
            options={
                "verbose_name": "Resource",
                "verbose_name_plural": "Resources",
                "ordering": ["order", "-created_date"],
            },
        ),
        migrations.CreateModel(
            name="ResourceView",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("viewed_date", models.DateTimeField(auto_now_add=True)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("user_agent", models.TextField(blank=True)),
                (
                    "resource",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="views",
                        to="roshan.resource",
                    ),
                ),
            ],
            options={
                "verbose_name": "Resource View",
                "verbose_name_plural": "Resource Views",
            },
        ),
    ]
