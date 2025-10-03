from django.db import models
from django.utils.text import slugify
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
# SITE-WIDE CONFIGURATION MODEL
# =========================================================================


class SiteConfiguration(models.Model):
    # --- Hero Section ---
    hero_greeting = models.CharField(max_length=100, default="HIII, IT'S ME")
    hero_name = models.CharField(max_length=100, default="Roshan Damor")
    hero_tagline = models.CharField(max_length=200, default="I am a Web Developer")

    # --- Hero Stats ---
    hero_projects_stat = models.CharField(max_length=10, default="25+")
    hero_internships_stat = models.CharField(max_length=10, default="3+")
    hero_articles_stat = models.CharField(max_length=10, default="15+")

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


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    summary = models.TextField(
        help_text="A short summary displayed on the project list page."
    )
    content = HTMLField(
        help_text="The main detailed content for the project detail page."
    )
    cover_image = models.ImageField(upload_to="project_covers/")
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


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="project_images/")
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
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    icon = models.CharField(max_length=50)
    summary = models.TextField()
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


# =========================================================================
# CODE TOGETHER PAGE MODELS
# =========================================================================


class CodeTogetherConfiguration(models.Model):

    # --- Page Header ---
    page_title = models.CharField(
        max_length=255, default="Let's Build <span>Together</span>"
    )
    intro_paragraph = models.TextField(
        default="I'm always excited to collaborate on innovative projects. Here's a look at what I'm passionate about building."
    )
    interests_content = HTMLField(
        help_text="Content describing your collaboration interests with HTML support"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Code Together Configuration"
        verbose_name_plural = "Code Together Configuration"

    def __str__(self):
        return "Code Together Page Configuration"

    def save(self, *args, **kwargs):
        """Ensure only one instance exists."""
        if not self.pk and CodeTogetherConfiguration.objects.exists():
            # Update existing instance instead of creating new one
            existing = CodeTogetherConfiguration.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)


class CollaborationProposal(models.Model):

    # --- Personal Information ---
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    github_id = models.CharField(
        max_length=100, blank=True, help_text="GitHub username (optional)"
    )
    linkedin_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="LinkedIn profile URL or username (optional)",
    )
    proposal = HTMLField(
        help_text="Detailed project proposal or collaboration idea with HTML support"
    )  # Changed to HTMLField
    status_choices = [
        ("pending", "Pending Review"),
        ("reviewing", "Under Review"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
        ("completed", "Completed"),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default="pending")
    submitted_date = models.DateTimeField(auto_now_add=True)
    reviewed_date = models.DateTimeField(blank=True, null=True)
    admin_notes = HTMLField(blank=True, help_text="Internal notes for admin use")

    class Meta:
        ordering = ["-submitted_date"]
        verbose_name = "Collaboration Proposal"
        verbose_name_plural = "Collaboration Proposals"

    def __str__(self):
        return f"Proposal from {self.full_name} - {self.get_status_display()}"


class Testimonial(models.Model):
    author_name = models.CharField(max_length=100)
    author_role = models.CharField(
        max_length=200, help_text="e.g., 'Project Manager @ TechCorp'"
    )
    author_image = models.ImageField(
        upload_to="testimonials/",
        blank=True,
        null=True,
        help_text="Author's profile picture (optional)",
    )
    quote = HTMLField(
        help_text="The testimonial quote with HTML support"
    )  # Changed to HTMLField
    is_featured = models.BooleanField(
        default=True, help_text="Display this testimonial on the Code Together page"
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Display order (lower numbers appear first)"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_date"]
        verbose_name = "Testimonial"
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
