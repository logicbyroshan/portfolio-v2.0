from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField
from portfolio.models import Category
from roshan.models import AboutMeConfiguration
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


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    summary = models.TextField(help_text="A short excerpt for the blog list page.")
    content = HTMLField()
    cover_image = models.ImageField(upload_to="blog_covers/")
    categories = models.ManyToManyField(
        Category, limit_choices_to={"category_type": Category.CategoryType.BLOG}
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_date"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.summary = sanitize_html(self.summary)
        self.content = sanitize_html(self.content)
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
