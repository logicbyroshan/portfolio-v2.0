from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField
from portfolio.models import Category
from roshan.models import AboutMeConfiguration
from django.core.exceptions import ValidationError
import bleach
import math
import re
import os

ALLOWED_TAGS = ["b", "i", "strong", "em", "u", "a", "br", "p", "ul", "ol", "li", "span"]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
    "span": ["style"],
}


def validate_image_file(file):
    """
    Validates that the uploaded file is an image with allowed extensions.
    Supports all common image formats including modern ones like WebP.
    """
    valid_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp",
        ".svg",
        ".tiff",
        ".tif",
        ".ico",
        ".avif",
    ]
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(
            f"Only image files are allowed. Supported formats: "
            f"{', '.join(valid_extensions).upper().replace('.', '')}"
        )


def sanitize_html(value):
    if value:
        return bleach.clean(
            value, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True
        )
    return value


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    summary = models.TextField(help_text="A short excerpt for the blog list page.")
    content = HTMLField()
    reading_time = models.PositiveIntegerField(default=0)
    cover_image = models.FileField(
        upload_to="blog_covers/",
        validators=[validate_image_file],
        help_text="Upload blog cover image (supports JPG, PNG, WebP, SVG, etc.)",
    )
    categories = models.ManyToManyField(
        Category, limit_choices_to={"category_type": Category.CategoryType.BLOG}
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_date"]

    def calculate_reading_time(self):
        """Estimate reading time based on word count (avg: 200 words/minute)."""
        # Remove HTML tags from TinyMCE content
        text = re.sub(r"<[^>]+>", "", self.content)
        word_count = len(text.split())
        minutes = math.ceil(word_count / 200)
        return minutes if minutes > 0 else 1

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.summary = sanitize_html(self.summary)
        self.content = sanitize_html(self.content)
        # Calculate reading time automatically
        self.reading_time = self.calculate_reading_time()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def author_name(self):
        """Get author name from SiteConfiguration."""
        try:
            from portfolio.models import SiteConfiguration

            site_config = SiteConfiguration.objects.first()
            return site_config.hero_name if site_config else "Roshan Damor"
        except Exception:
            return "Roshan Damor"

    @property
    def author_avatar(self):
        """Get author avatar from AboutMeConfiguration."""
        try:
            about_config = AboutMeConfiguration.objects.first()
            return (
                about_config.profile_image
                if about_config and about_config.profile_image
                else None
            )
        except AboutMeConfiguration.DoesNotExist:
            return None


class Comment(models.Model):
    post = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_date"]

    def __str__(self):
        return f"Comment by {self.author_name} on {self.post.title}"

    @property
    def total_likes(self):
        """Get total number of likes for this comment."""
        return self.user_likes.count()

    def is_liked_by_user(self, user):
        """Check if a specific user has liked this comment."""
        if user.is_authenticated:
            return self.user_likes.filter(user=user).exists()
        return False


class CommentLike(models.Model):
    """Model to track individual user likes on blog comments."""

    comment = models.ForeignKey(
        Comment, related_name="user_likes", on_delete=models.CASCADE
    )
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "user")  # Prevent duplicate likes
        verbose_name = "Comment Like"
        verbose_name_plural = "Comment Likes"

    def __str__(self):
        return f"{self.user.username} likes comment on {self.comment.post.title}"
