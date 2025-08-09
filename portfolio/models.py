from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField # <--- IMPORT CHANGED

# =========================================================================
# HELPER/TAGGING MODELS
# =========================================================================

class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='tech_icons/', blank=True, null=True, help_text="Optional icon for the technology")

    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ['name']

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, editable=False)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================================================================
# CORE CONTENT MODELS (PROJECTS, BLOGS, EXPERIENCE)
# =========================================================================

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    summary = models.TextField(help_text="A short summary displayed on the project list page.")
    content = HTMLField(help_text="The main detailed content for the project detail page.") # <--- FIELD CHANGED
    cover_image = models.ImageField(upload_to='project_covers/')
    
    technologies = models.ManyToManyField(Technology, related_name="projects")
    categories = models.ManyToManyField(Category, related_name="projects")
    
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
    content = HTMLField() # <--- FIELD CHANGED
    cover_image = models.ImageField(upload_to='blog_covers/')
    categories = models.ManyToManyField(Category, related_name="blogs")
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
    is_approved = models.BooleanField(default=True, help_text="Uncheck to hide the comment from the site.")

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
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if this is your current role.")
    
    summary = models.TextField(help_text="A brief summary shown on the experience list page.")
    responsibilities = HTMLField() # <--- FIELD CHANGED
    achievements = HTMLField() # <--- FIELD CHANGED

    technologies = models.ManyToManyField(Technology, related_name="experiences")
    experience_type = models.CharField(max_length=2, choices=ExperienceType.choices, default=ExperienceType.FULL_TIME)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.role} at {self.company_name}"

# =========================================================================
# SITE CONFIGURATION & OTHER MODELS (FAQ, SKILLS)
# =========================================================================

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Order in which to display the FAQ.")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question

class Skill(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class (e.g., 'fa-solid fa-code')")
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