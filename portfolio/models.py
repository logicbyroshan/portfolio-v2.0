from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField

# =========================================================================
# SITE-WIDE CONFIGURATION MODEL
# =========================================================================

class SiteConfiguration(models.Model):
    """
    Model to hold site-wide settings and content for static sections.
    There will only ever be one instance of this model.
    """
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
    linkedin_url = models.URLField(blank=True, default="https://www.linkedin.com/in/logicbyroshan")
    youtube_url = models.URLField(blank=True, default="https://www.youtube.com/channel/logicbyroshan")
    instagram_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    
    # --- Contact Information ---
    email = models.EmailField(blank=True, default="contact@roshanproject.site")
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True, default="India")
    
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
    icon = models.ImageField(upload_to='tech_icons/', blank=True, null=True)
    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ['name']
    def __str__(self):
        return self.name

class Category(models.Model):
    """IMPROVED: Now includes a type to distinguish between Project and Blog categories."""
    class CategoryType(models.TextChoices):
        PROJECT = 'PRO', 'Project'
        BLOG = 'BLG', 'Blog'
        EXPERIENCE = 'EXP', 'Experience'
        OTHER = 'OTH', 'Other'

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, editable=False)
    category_type = models.CharField(max_length=3, choices=CategoryType.choices)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
        unique_together = ('name', 'category_type') # Prevents "Web Dev" for both Blog and Project

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"




class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    summary = HTMLField(help_text="A short summary displayed on the project list page.")
    content = HTMLField(help_text="The main detailed content for the project detail page.")
    cover_image = models.ImageField(upload_to='project_covers/')
    technologies = models.ManyToManyField(Technology, related_name="projects")
    categories = models.ManyToManyField(Category, limit_choices_to={'category_type': Category.CategoryType.PROJECT})
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_date']
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"Image for {self.project.title}"

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    summary = HTMLField(help_text="A short excerpt for the blog list page.")
    content = HTMLField()
    cover_image = models.ImageField(upload_to='blog_covers/')
    categories = models.ManyToManyField(Category, limit_choices_to={'category_type': Category.CategoryType.BLOG})
    created_date = models.DateTimeField(auto_now_add=True)
    author_name = models.CharField(max_length=100, default="Roshan Damor")
    author_avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    class Meta:
        ordering = ['-created_date']
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100)
    body = HTMLField()
    likes = models.PositiveIntegerField(default=0)  # Keep for backward compatibility
    created_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created_date']
    
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

class ProjectComment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100, default="Anonymous")
    body = HTMLField()
    likes = models.PositiveIntegerField(default=0)  # Keep for backward compatibility
    created_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created_date']
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
    class ExperienceType(models.TextChoices):
        FULL_TIME = 'FT', 'Full-Time'
        INTERNSHIP = 'IN', 'Internship'
        FREELANCE = 'FR', 'Freelance'
    company_name = models.CharField(max_length=200)
    company_url = models.URLField(blank=True, null=True)
    role = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    summary = HTMLField()
    responsibilities = HTMLField()
    achievements = HTMLField()
    technologies = models.ManyToManyField(Technology, related_name="experiences")
    experience_type = models.CharField(max_length=2, choices=ExperienceType.choices, default=ExperienceType.FULL_TIME)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.role} at {self.company_name}"


# =========================================================================
# NEW DYNAMIC SECTION MODELS
# =========================================================================

class Service(models.Model):
    """NEW: For a service listed in the 'About Me' section."""
    title = models.CharField(max_length=100)
    description = HTMLField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class (e.g., 'fas fa-code')")
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.title


class Resume(models.Model):
    """Enhanced Resume modal with dynamic content."""
    # Main resume file and preview
    preview_image = models.ImageField(
        upload_to='resume/', 
        help_text="Upload a preview image of your resume (JPG/PNG recommended)"
    )
    downloadable_file = models.FileField(
        upload_to='resume/', 
        help_text="Upload your resume PDF file"
    )
    
    # Additional resume information
    title = models.CharField(max_length=200, default="My Resume")
    description = HTMLField(
        blank=True, 
        default="Download my latest resume to learn more about my experience and skills."
    )
    last_updated = models.DateTimeField(auto_now=True)
    
    # Resume stats/highlights
    years_experience = models.CharField(max_length=10, blank=True, default="3+")
    total_projects = models.CharField(max_length=10, blank=True, default="25+")
    technologies_used = models.CharField(max_length=10, blank=True, default="15+")
    
    def __str__(self):
        return self.title

class VideoResume(models.Model):
    """Model for the Video Resume modal."""
    youtube_embed_url = models.URLField(help_text="The full YouTube embed URL (e.g., https://www.youtube.com/embed/VIDEO_ID)")
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
    message = HTMLField()
    submitted_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    class Meta:
        ordering = ['-submitted_date']
        verbose_name = "Contact Submission"
    def __str__(self):
        return f"Message from {self.name}"

# --- SKILL MODELS (enhanced with categories) ---
class Skill(models.Model):
    # Skill Category Choices
    class SkillCategory(models.TextChoices):
        FRONTEND = 'FRONTEND', 'Frontend Development'
        BACKEND = 'BACKEND', 'Backend Development'
        DATABASE = 'DATABASE', 'Database & Storage'
        DEVOPS = 'DEVOPS', 'DevOps & Deployment'
        MOBILE = 'MOBILE', 'Mobile Development'
        AI_ML = 'AI_ML', 'AI & Machine Learning'
        DESIGN = 'DESIGN', 'Design & UI/UX'
        TOOLS = 'TOOLS', 'Development Tools'
        TESTING = 'TESTING', 'Testing & QA'
        OTHER = 'OTHER', 'Other Skills'

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    category = models.CharField(
        max_length=20, 
        choices=SkillCategory.choices, 
        default=SkillCategory.OTHER,
        help_text="The category this skill belongs to"
    )
    icon = models.CharField(max_length=50)
    summary = HTMLField()
    technologies = models.ManyToManyField(Technology, through='SkillTechnologyDetail')
    
    class Meta:
        ordering = ['category', 'title']
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class SkillTechnologyDetail(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    learning_journey = HTMLField()
    class Meta:
        unique_together = ('skill', 'technology')
    def __str__(self):
        return f"{self.technology.name} in {self.skill.title}"

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = HTMLField()
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.question

class Achievement(models.Model):
    # Choices for the type of achievement for easy filtering
    class AchievementType(models.TextChoices):
        CERTIFICATION = 'CERT', 'Certification'
        AWARD = 'AWRD', 'Award'
        PUBLICATION = 'PUBL', 'Publication'
        HONOR = 'HONR', 'Honor'

    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    summary = HTMLField(help_text="A brief description of the achievement.")
    date_issued = models.DateField()
    credential_url = models.URLField(max_length=255, blank=True, null=True, help_text="Link to verify the credential, if available.")
    image = models.ImageField(upload_to='achievements/', blank=True, null=True, help_text="Optional: A scan or image of the certificate/award.")
    category = models.CharField(max_length=4, choices=AchievementType.choices, default=AchievementType.CERTIFICATION)

    class Meta:
        ordering = ['-date_issued'] # Show newest first by default

    def __str__(self):
        return f"{self.title} from {self.issuing_organization}"


# =========================================================================
# ABOUT ME PAGE CONFIGURATION MODEL
# =========================================================================

class AboutMeConfiguration(models.Model):
    """
    Model to hold content and settings for the About Me page.
    There will only ever be one instance of this model.
    """
    # --- Page Header ---
    page_title = HTMLField(default="A Bit More <span>About Me</span>")
    intro_paragraph = models.TextField(
        max_length=500,
        default="This is my story, my journey, and what drives me."
    )
    
    # --- Profile Section ---
    profile_image = models.ImageField(
        upload_to='about/',
        blank=True,
        null=True,
        help_text="Profile image for About Me page"
    )
    detailed_description = HTMLField(
        default="""<ul>
            <li><strong>Mission:</strong> To build software that is not only functional but also intuitive and impactful.</li>
            <li><strong>Interests:</strong> Beyond coding, I'm passionate about AI ethics, open-source contribution, and exploring the intersection of technology and art.</li>
        </ul>""",
        help_text="Detailed description with HTML support"
    )
    
    # --- Action Card 1: Music ---
    action1_title = models.CharField(max_length=100, default="My Song Playlists")
    action1_description = models.TextField(
        max_length=300,
        default="Discover the music that fuels my coding sessions and creative work."
    )
    action1_button_text = models.CharField(max_length=50, default="Listen Now")
    
    # --- Action Card 2: Community ---
    action2_title = models.CharField(max_length=100, default="Join My Community")
    action2_description = models.TextField(
        max_length=300,
        default="Let's connect, share ideas, and build amazing things together."
    )
    action2_button_text = models.CharField(max_length=50, default="Join Community")
    action2_link = models.URLField(
        default="https://risetogethr.tech",
        help_text="External link for community"
    )
    
    # --- Action Card 3: Resources ---
    action3_title = models.CharField(max_length=100, default="View My Resources")
    action3_description = models.TextField(
        max_length=300,
        default="A curated list of tools, articles, and learning materials that I find valuable."
    )
    action3_button_text = models.CharField(max_length=50, default="Explore Resources")
    
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
# CODE TOGETHER PAGE MODELS
# =========================================================================

class CodeTogetherConfiguration(models.Model):
    """
    Model to hold content and settings for the Code Together page.
    There will only ever be one instance of this model.
    """
    # --- Page Header ---
    page_title = HTMLField(default="Let's Build <span>Together</span>")
    intro_paragraph = models.TextField(
        max_length=500,
        default="I'm always excited to collaborate on innovative projects. Here's a look at what I'm passionate about building."
    )
    
    # --- Interests Section ---
    interests_content = HTMLField(
        default="""<ul>
            <li><strong>AI-Powered Web Apps:</strong> Integrating ML models into practical, user-facing applications.</li>
            <li><strong>Open-Source Tools:</strong> Creating libraries or utilities that can help other developers.</li>
            <li><strong>Full-Stack Solutions:</strong> From database design to responsive frontends.</li>
            <li><strong>API Development:</strong> Building robust and scalable RESTful APIs.</li>
        </ul>""",
        help_text="Content describing your collaboration interests with HTML support"
    )
    
    # --- Meta Information ---
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
    """
    Model to store collaboration proposals submitted through the Code Together form.
    """
    # --- Personal Information ---
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    github_id = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="GitHub username (optional)"
    )
    linkedin_id = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="LinkedIn profile URL or username (optional)"
    )
    
    # --- Proposal Details ---
    proposal = HTMLField(help_text="Detailed project proposal or collaboration idea")
    
    # --- Status and Management ---
    status_choices = [
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=status_choices, 
        default='pending'
    )
    
    # --- Timestamps ---
    submitted_date = models.DateTimeField(auto_now_add=True)
    reviewed_date = models.DateTimeField(blank=True, null=True)
    
    # --- Admin Notes ---
    admin_notes = HTMLField(
        blank=True, 
        help_text="Internal notes for admin use"
    )
    
    class Meta:
        ordering = ['-submitted_date']
        verbose_name = "Collaboration Proposal"
        verbose_name_plural = "Collaboration Proposals"
    
    def __str__(self):
        return f"Proposal from {self.full_name} - {self.get_status_display()}"


class Testimonial(models.Model):
    """
    Model to store testimonials for the Code Together page.
    """
    author_name = models.CharField(max_length=100)
    author_role = models.CharField(
        max_length=200,
        help_text="e.g., 'Project Manager @ TechCorp'"
    )
    author_image = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True,
        help_text="Author's profile picture (optional)"
    )
    quote = models.TextField(
        max_length=500,
        help_text="The testimonial quote"
    )
    
    # --- Management ---
    is_featured = models.BooleanField(
        default=True,
        help_text="Display this testimonial on the Code Together page"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    
    # --- Timestamps ---
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_date']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return f"Testimonial by {self.author_name}"


# =========================================================================
# RESOURCES PAGE MODELS
# =========================================================================

class ResourcesConfiguration(models.Model):
    """
    Model to hold content and settings for the Resources page.
    There will only ever be one instance of this model.
    """
    # --- Page Header ---
    page_title = HTMLField(default="My Curated <span>Resources</span>")
    intro_paragraph = models.TextField(
        max_length=500,
        default="A collection of valuable articles, tools, videos, and courses that have helped me in my development journey."
    )
    
    # --- Resource Section Content ---
    resources_description = HTMLField(
        default="""<p>These resources have been carefully curated based on my experience and their practical value in real-world development scenarios. 
        Each resource has been personally tested and found valuable for professional growth.</p>""",
        help_text="Additional description content for the resources section",
        blank=True
    )
    
    # --- Display Settings ---
    resources_per_page = models.PositiveIntegerField(
        default=12,
        help_text="Number of resources to display per page"
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
    description = models.TextField(
        max_length=200,
        blank=True,
        help_text="Brief description of this resource category"
    )
    icon = models.CharField(
        max_length=50,
        default="fa-solid fa-folder",
        help_text="Font Awesome icon class (e.g., 'fa-solid fa-code')"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order for category filtering"
    )
    
    class Meta:
        verbose_name_plural = "Resource Categories"
        ordering = ['order', 'name']
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Resource(models.Model):
    """
    Model to store different types of resources including videos, PDFs, articles, tools, etc.
    """
    # --- Resource Type Choices ---
    class ResourceType(models.TextChoices):
        ARTICLE = 'ART', 'Article'
        VIDEO = 'VID', 'Video'
        PDF = 'PDF', 'PDF Document'
        TOOL = 'TOL', 'Tool/Website'
        COURSE = 'CRS', 'Course'
        BOOK = 'BOK', 'Book'
        TUTORIAL = 'TUT', 'Tutorial'
        DOCUMENTATION = 'DOC', 'Documentation'
        REPOSITORY = 'REP', 'Code Repository'
        OTHER = 'OTH', 'Other'
    
    # --- Basic Information ---
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    description = models.TextField(
        max_length=300,
        help_text="Brief description of the resource"
    )
    
    # --- Resource Content ---
    resource_type = models.CharField(
        max_length=3,
        choices=ResourceType.choices,
        default=ResourceType.ARTICLE
    )
    link = models.URLField(
        blank=True,
        null=True,
        help_text="External link to the resource"
    )
    
    # --- File Uploads (for PDFs and other downloadable content) ---
    file_upload = models.FileField(
        upload_to='resources/files/',
        blank=True,
        null=True,
        help_text="Upload file for downloadable resources (PDFs, documents, etc.)"
    )
    
    # --- Video Embedding ---
    youtube_embed_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="YouTube video ID for embedding (e.g., 'dQw4w9WgXcQ')"
    )
    vimeo_embed_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Vimeo video ID for embedding"
    )
    custom_embed_code = HTMLField(
        blank=True,
        help_text="Custom embed code for other video platforms or widgets"
    )
    
    # --- Preview and Thumbnail ---
    thumbnail = models.ImageField(
        upload_to='resources/thumbnails/',
        blank=True,
        null=True,
        help_text="Thumbnail image for the resource"
    )
    preview_image = models.ImageField(
        upload_to='resources/previews/',
        blank=True,
        null=True,
        help_text="Preview image for PDFs or other documents"
    )
    
    # --- Categorization ---
    categories = models.ManyToManyField(
        ResourceCategory,
        related_name="resources",
        blank=True
    )
    technologies = models.ManyToManyField(
        Technology,
        related_name="resources",
        blank=True,
        help_text="Related technologies or tech stack"
    )
    
    # --- Additional Metadata ---
    author = models.CharField(
        max_length=100,
        blank=True,
        help_text="Original author or creator of the resource"
    )
    publication_date = models.DateField(
        blank=True,
        null=True,
        help_text="When the resource was originally published"
    )
    
    # --- Management ---
    is_featured = models.BooleanField(
        default=False,
        help_text="Display this resource prominently"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this resource should be displayed"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order within category"
    )
    
    # --- Rating and Feedback ---
    personal_rating = models.PositiveIntegerField(
        default=5,
        choices=[(i, f"{i} Stars") for i in range(1, 6)],
        help_text="Your personal rating of this resource (1-5 stars)"
    )
    
    # --- Timestamps ---
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_date']
        verbose_name = "Resource"
        verbose_name_plural = "Resources"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.get_resource_type_display()})"
    
    @property
    def has_video_embed(self):
        """Check if resource has any video embed information."""
        return bool(self.youtube_embed_id or self.vimeo_embed_id or self.custom_embed_code)
    
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
            return f"https://img.youtube.com/vi/{self.youtube_embed_id}/maxresdefault.jpg"
        return None


class ResourceView(models.Model):
    """
    Model to track resource views and analytics.
    """
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='views'
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
# COMMENT LIKE MODELS
# =========================================================================

class CommentLike(models.Model):
    """Model to track individual user likes on blog comments."""
    comment = models.ForeignKey(Comment, related_name='user_likes', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('comment', 'user')  # Prevent duplicate likes
        verbose_name = "Comment Like"
        verbose_name_plural = "Comment Likes"
    
    def __str__(self):
        return f"{self.user.username} likes comment on {self.comment.post.title}"


class ProjectCommentLike(models.Model):
    """Model to track individual user likes on project comments."""
    comment = models.ForeignKey(ProjectComment, related_name='user_likes', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('comment', 'user')  # Prevent duplicate likes
        verbose_name = "Project Comment Like"
        verbose_name_plural = "Project Comment Likes"
    
    def __str__(self):
        return f"{self.user.username} likes comment on {self.comment.project.title}"