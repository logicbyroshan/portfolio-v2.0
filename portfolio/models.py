from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField
import bleach
from django.core.exceptions import ValidationError
import os

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
# SITE-WIDE CONFIGURATION MODEL
# =========================================================================


class SiteConfiguration(models.Model):
    # --- Hero Section ---
    # hero_greeting removed - now using static "HII It's Me" text
    hero_name = models.CharField(max_length=100, default="Roshan Damor")
    # hero_tagline removed - now using static "Full Stack AI Developer" text

    # --- Hero Stats ---
    hero_leetcode_rating = models.CharField(max_length=10, default="1800+")
    hero_opensource_contributions = models.CharField(max_length=10, default="50+")
    hero_hackathons_count = models.CharField(max_length=10, default="12+")

    # --- Social Media Links ---
    twitter_url = models.URLField(blank=True, default="https://x.com/logicbyroshan")
    github_url = models.URLField(blank=True, default="https://github.com/logicbyroshan")
    linkedin_url = models.URLField(
        blank=True, default="https://www.linkedin.com/in/logicbyroshan"
    )
    youtube_url = models.URLField(
        blank=True, default="https://www.youtube.com/channel/logicbyroshan"
    )
    instagram_url = models.URLField(
        blank=True, default="https://www.instagram.com/logicbyroshan"
    )
    facebook_url = models.URLField(
        blank=True, default="https://www.facebook.com/logicbyroshan"
    )

    email = models.EmailField(blank=True, default="contact@roshandamor.me")
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True, default="Bhopal, India")

    # ... and so on for every other section ...

    class Meta:
        verbose_name = "Site Configuration"

    def __str__(self):
        return "Site Configuration"


# =========================================================================
# HELPER/TAGGING MODELS
# =========================================================================


class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to="tech_icons/", blank=True, null=True)
    category = models.ForeignKey(
        "Category",
        limit_choices_to={"category_type": "SKL"},
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    class CategoryType(models.TextChoices):
        PROJECT = "PRO", "Project"
        BLOG = "BLG", "Blog"
        EXPERIENCE = "EXP", "Experience"
        SKILL = "SKL", "Skill"
        ACHIEVEMENT = "ACH", "Achievement"
        OTHER = "OTH", "Other"

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, editable=False)
    category_type = models.CharField(max_length=3, choices=CategoryType.choices)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]
        unique_together = (
            "name",
            "category_type",
        )  # Prevents "Web Dev" for both Blog and Project

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"

def validate_image_file(file):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.svg']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Only JPG, JPEG, PNG, or SVG files are allowed.")

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    summary = models.TextField(
        help_text="A short summary displayed on the project list page."
    )
    content = HTMLField(
        help_text="The main detailed content for the project detail page."
    )
    cover_image = models.FileField(upload_to="project_covers/",  validators=[validate_image_file], blank=True, null=True)
    youtube_url = models.URLField(
        blank=True, null=True, help_text="YouTube video URL for project demonstration"
    )
    technologies = models.ManyToManyField(Technology, related_name="projects")
    categories = models.ManyToManyField(
        Category, limit_choices_to={"category_type": Category.CategoryType.PROJECT}
    )
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while type(self).objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # sanitize fields
        self.summary = sanitize_html(self.summary)
        self.content = sanitize_html(self.content)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def youtube_video_id(self):
        """Extract YouTube video ID from the URL"""
        if not self.youtube_url:
            return None

        import re

        # Handle different YouTube URL formats
        patterns = [
            r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]+)",
            r"youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                return match.group(1)
        return None

    @property
    def youtube_thumbnail_url(self):
        """Get YouTube video thumbnail URL"""
        video_id = self.youtube_video_id
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return None


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, related_name="images", on_delete=models.CASCADE
    )
    image = models.FileField(upload_to="project_images/",  validators=[validate_image_file])
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.project.title}"


class ProjectComment(models.Model):
    project = models.ForeignKey(
        Project, related_name="comments", on_delete=models.CASCADE
    )
    author_name = models.CharField(max_length=100, default="Anonymous")
    body = models.TextField()
    # likes = models.PositiveIntegerField(default=0) # Removed, `total_likes` property handles this
    created_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_date"]
        verbose_name = "Project Comment"
        verbose_name_plural = "Project Comments"

    def __str__(self):
        return f"Comment by {self.author_name} on {self.project.title}"

    @property
    def total_likes(self):
        """Get total number of likes for this comment."""
        return self.user_likes.count()

    def is_liked_by_user(self, user):
        """Check if a specific user has liked this comment."""
        if user.is_authenticated:
            return self.user_likes.filter(user=user).exists()
        return False


class Experience(models.Model):
    company_name = models.CharField(max_length=200)
    company_url = models.URLField(blank=True, null=True)
    role = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    summary = models.TextField(
        help_text="A brief summary of your role and contributions."
    )
    responsibilities = HTMLField()
    achievements = HTMLField()
    technologies = models.ManyToManyField(Technology, related_name="experiences")
    experience_type = models.ForeignKey(
        Category,
        limit_choices_to={"category_type": Category.CategoryType.EXPERIENCE},
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["-start_date"]

    def save(self, *args, **kwargs):
        self.summary = sanitize_html(self.summary)
        self.responsibilities = sanitize_html(self.responsibilities)
        self.achievements = sanitize_html(self.achievements)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.role} at {self.company_name}"


# =========================================================================
# NEW DYNAMIC SECTION MODELS
# =========================================================================


class Resume(models.Model):
    """Enhanced Resume modal with dynamic content."""

    # Main resume file and preview
    preview_image = models.ImageField(
        upload_to="resume/",
        help_text="Upload a preview image of your resume (JPG/PNG recommended)",
    )
    downloadable_file = models.FileField(
        upload_to="resume/", help_text="Upload your resume PDF file"
    )

    # Additional resume information
    title = models.CharField(max_length=200, default="My Resume")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class VideoResume(models.Model):
    """Model for the Video Resume modal."""

    youtube_embed_url = models.URLField(
        help_text="The full YouTube embed URL (e.g., https://www.youtube.com/embed/VIDEO_ID)"
    )

    def __str__(self):
        return "Video Resume"


class NewsletterSubscriber(models.Model):
    """NEW: To store newsletter subscribers."""

    email = models.EmailField(unique=True)
    subscribed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class ContactSubmission(models.Model):
    """NEW: To store contact form submissions."""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_urgent = models.BooleanField(
        default=False, help_text="Mark as urgent for priority response"
    )
    submitted_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_date"]
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"Message from {self.name}"


# --- SKILL MODELS (enhanced with categories) ---
class Skill(models.Model):
    SKILL_CATEGORIES = [
        ("languages_frameworks", "Languages & Frameworks"),
        ("backend_database", "Backend & Database"),
        ("tools_platforms", "Tools & Platforms"),
        ("soft_skills", "Soft Skills"),
    ]

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    category = models.CharField(
        max_length=50,
        choices=SKILL_CATEGORIES,
        default="languages_frameworks",
        help_text="Category for organizing skills on home page",
    )
    icon = models.CharField(max_length=50)
    learning_journey = HTMLField(
        blank=True, help_text="Detailed learning journey and experience with this skill"
    )
    order = models.PositiveIntegerField(default=0)
    technologies = models.ManyToManyField(Technology, blank=True)

    # New fields for skill detail page
    proficiency_level = models.CharField(
        max_length=20,
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("advanced", "Advanced"),
            ("expert", "Expert"),
        ],
        default="intermediate",
    )
    years_of_experience = models.PositiveIntegerField(
        default=1, help_text="Years of experience with this skill"
    )
    is_featured = models.BooleanField(
        default=False, help_text="Display this skill prominently on the home page"
    )

    class Meta:
        ordering = ["order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while type(self).objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def related_projects_count(self):
        """Get count of projects using technologies from this skill"""
        return (
            Project.objects.filter(technologies__in=self.technologies.all())
            .distinct()
            .count()
        )

    @property
    def technology_list(self):
        """Get comma-separated list of technology names"""
        return ", ".join([tech.name for tech in self.technologies.all()])


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question


class Achievement(models.Model):
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    summary = models.TextField(
        help_text="A brief description of the achievement, can include HTML."
    )  # Changed to TextField
    date_issued = models.DateField()
    credential_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Link to verify the credential, if available.",
    )
    image = models.ImageField(
        upload_to="achievements/",
        blank=True,
        null=True,
        help_text="Optional: A scan or image of the certificate/award.",
    )
    category = models.ForeignKey(
        Category,
        limit_choices_to={"category_type": Category.CategoryType.ACHIEVEMENT},
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["-date_issued"]  # Show newest first by default

    def save(self, *args, **kwargs):
        self.summary = sanitize_html(self.summary)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} from {self.issuing_organization}"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"Testimonial by {self.author_name}"


# =========================================================================
# COMMENT LIKE MODELS
# =========================================================================


class ProjectCommentLike(models.Model):
    """Model to track individual user likes on project comments."""

    comment = models.ForeignKey(
        ProjectComment, related_name="user_likes", on_delete=models.CASCADE
    )
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "user")  # Prevent duplicate likes
        verbose_name = "Project Comment Like"
        verbose_name_plural = "Project Comment Likes"

    def __str__(self):
        return f"{self.user.username} likes comment on {self.comment.project.title}"
