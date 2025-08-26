from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField
from solo.models import SingletonModel

# =========================================================================
# SITE-WIDE CONFIGURATION (SINGLETON MODEL)
# =========================================================================

class SiteConfiguration(SingletonModel):
    """
    Singleton model to hold site-wide settings and content for static sections.
    There will only ever be one instance of this model.
    """
    # --- Hero Section ---
    hero_greeting = models.CharField(max_length=100, default="HIII, IT'S ME")
    hero_name = models.CharField(max_length=100, default="Roshan Damor")
    hero_tagline = models.CharField(max_length=200, default="I am a Web Developer")
    hero_bio = models.TextField(default='GREETINGS, ALL DIGITAL EXPLORERS! ...')
    
    # --- Hero Stats ---
    hero_projects_stat = models.CharField(max_length=10, default="25+")
    hero_internships_stat = models.CharField(max_length=10, default="3+")
    hero_articles_stat = models.CharField(max_length=10, default="15+")

    # --- Section Titles & Descriptions ---
    about_title = models.CharField(max_length=200, default="About Me")
    about_description = models.TextField(blank=True)
    now_title = models.CharField(max_length=200, default="What I'm Doing Now")
    now_description = models.TextField(blank=True)
    skills_title = models.CharField(max_length=200, default="My Tech Stack")
    skills_description = models.TextField(blank=True)
    experience_title = models.CharField(max_length=200, default="Where I've Worked")
    experience_description = models.TextField(blank=True)
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
    summary = models.TextField(help_text="A short summary displayed on the project list page.")
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
    summary = models.TextField(help_text="A short excerpt for the blog list page.")
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
    body = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)
    class Meta:
        ordering = ['created_date']
    def __str__(self):
        return f"Comment by {self.author_name} on {self.post.title}"

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
    summary = models.TextField()
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
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class (e.g., 'fas fa-code')")
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.title


class Resume(SingletonModel):
    """NEW: Singleton model for the Resume modal."""
    preview_image = models.ImageField(upload_to='resume/')
    downloadable_file = models.FileField(upload_to='resume/')
    def __str__(self):
        return "My Resume"

class VideoResume(SingletonModel):
    """NEW: Singleton model for the Video Resume modal."""
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
    message = models.TextField()
    submitted_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    class Meta:
        ordering = ['-submitted_date']
        verbose_name = "Contact Submission"
    def __str__(self):
        return f"Message from {self.name}"

# --- SKILL MODELS (largely unchanged) ---
class Skill(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    icon = models.CharField(max_length=50)
    summary = models.TextField()
    technologies = models.ManyToManyField(Technology, through='SkillTechnologyDetail')
    class Meta:
        ordering = ['title']
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class SkillTechnologyDetail(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    learning_journey = models.TextField()
    class Meta:
        unique_together = ('skill', 'technology')
    def __str__(self):
        return f"{self.technology.name} in {self.skill.title}"

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
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
    summary = models.TextField(help_text="A brief description of the achievement.")
    date_issued = models.DateField()
    credential_url = models.URLField(max_length=255, blank=True, null=True, help_text="Link to verify the credential, if available.")
    image = models.ImageField(upload_to='achievements/', blank=True, null=True, help_text="Optional: A scan or image of the certificate/award.")
    category = models.CharField(max_length=4, choices=AchievementType.choices, default=AchievementType.CERTIFICATION)

    class Meta:
        ordering = ['-date_issued'] # Show newest first by default

    def __str__(self):
        return f"{self.title} from {self.issuing_organization}"