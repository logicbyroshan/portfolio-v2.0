import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import (
    SiteConfiguration, Technology, Category, Project, ProjectImage, Blog, Comment, 
    Experience, FAQ, Skill, SkillTechnologyDetail, Achievement, Resume, VideoResume,
    NewsletterSubscriber, ContactSubmission, AboutMeConfiguration,
    CodeTogetherConfiguration, CollaborationProposal, Testimonial,
    ResourcesConfiguration, Resource, ResourceCategory, ResourceView
)

# =========================================================================
# MODEL ADMINS
# =========================================================================

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    """Admin for the Site Configuration object."""
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_greeting', 'hero_name', 'hero_tagline')
        }),
        ('Hero Stats', {
            'fields': ('hero_projects_stat', 'hero_internships_stat', 'hero_articles_stat')
        }),
        ('Social Media Links', {
            'fields': ('twitter_url', 'github_url', 'linkedin_url', 'youtube_url', 'instagram_url', 'facebook_url')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'location')
        }),
    )

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    pass

@admin.register(VideoResume)
class VideoResumeAdmin(admin.ModelAdmin):
    pass


# =========================================================================
# INLINES
# =========================================================================
# (These remain the same as before)
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('author_name', 'body', 'is_approved', 'created_date')
    readonly_fields = ('created_date',)

class SkillTechnologyDetailInline(admin.TabularInline):
    model = SkillTechnologyDetail
    extra = 1

# =========================================================================
# REGULAR MODEL ADMIN CONFIGURATIONS
# =========================================================================

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type')
    list_filter = ('category_type',)
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = ('title', 'created_date')
    list_filter = ('categories', 'technologies')
    search_fields = ('title', 'summary')
    filter_horizontal = ('technologies', 'categories')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('title', 'created_date')
    list_filter = ('categories',)
    search_fields = ('title', 'summary')
    filter_horizontal = ('categories',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'post', 'created_date', 'is_approved')
    list_filter = ('is_approved', 'created_date')
    search_fields = ('author_name', 'body', 'post__title')
    actions = ['approve_comments']
    
    @admin.action(description='Mark selected comments as approved')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company_name', 'start_date', 'end_date')
    list_filter = ('experience_type',)
    search_fields = ('role', 'company_name')
    filter_horizontal = ('technologies',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    inlines = [SkillTechnologyDetailInline]
    list_display = ('title', 'category', 'icon')
    list_filter = ('category',)
    search_fields = ('title', 'summary')
    list_editable = ('category',)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_date')
    search_fields = ('email',)
    actions = ['export_as_csv']
    
    @admin.action(description='Export selected subscribers as CSV')
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_date', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'submitted_date')
    actions = ['mark_as_read']

    @admin.action(description='Mark selected submissions as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuing_organization', 'category', 'date_issued')
    list_filter = ('category', 'date_issued')
    search_fields = ('title', 'issuing_organization', 'summary')


@admin.register(AboutMeConfiguration)
class AboutMeConfigurationAdmin(admin.ModelAdmin):
    """Admin for the About Me Configuration object."""
    fieldsets = (
        ('Page Header', {
            'fields': ('page_title', 'intro_paragraph')
        }),
        ('Profile Section', {
            'fields': ('profile_image', 'detailed_description')
        }),
        ('Action Card 1: Music', {
            'fields': ('action1_title', 'action1_description', 'action1_button_text')
        }),
        ('Action Card 2: Community', {
            'fields': ('action2_title', 'action2_description', 'action2_button_text', 'action2_link')
        }),
        ('Action Card 3: Resources', {
            'fields': ('action3_title', 'action3_description', 'action3_button_text')
        }),
    )
    
    def has_add_permission(self, request):
        """Only allow adding if no instance exists."""
        return not AboutMeConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion to maintain singleton pattern."""
        return False


@admin.register(CodeTogetherConfiguration)
class CodeTogetherConfigurationAdmin(admin.ModelAdmin):
    """Admin for the Code Together Configuration object."""
    fieldsets = (
        ('Page Header', {
            'fields': ('page_title', 'intro_paragraph')
        }),
        ('Interests Section', {
            'fields': ('interests_content',)
        }),
    )
    
    def has_add_permission(self, request):
        """Only allow adding if no instance exists."""
        return not CodeTogetherConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion to maintain singleton pattern."""
        return False


@admin.register(CollaborationProposal)
class CollaborationProposalAdmin(admin.ModelAdmin):
    """Admin for collaboration proposals."""
    list_display = ('full_name', 'email', 'status', 'submitted_date', 'reviewed_date')
    list_filter = ('status', 'submitted_date')
    search_fields = ('full_name', 'email', 'github_id', 'linkedin_id')
    readonly_fields = ('submitted_date',)
    
    fieldsets = (
        ('Proposal Information', {
            'fields': ('full_name', 'email', 'github_id', 'linkedin_id', 'proposal')
        }),
        ('Status & Management', {
            'fields': ('status', 'submitted_date', 'reviewed_date', 'admin_notes')
        }),
    )
    
    def mark_as_reviewing(self, request, queryset):
        queryset.update(status='reviewing')
    
    def mark_as_accepted(self, request, queryset):
        queryset.update(status='accepted')
    
    def mark_as_declined(self, request, queryset):
        queryset.update(status='declined')
    
    actions = ['mark_as_reviewing', 'mark_as_accepted', 'mark_as_declined']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin for testimonials."""
    list_display = ('author_name', 'author_role', 'is_featured', 'order', 'created_date')
    list_filter = ('is_featured', 'created_date')
    search_fields = ('author_name', 'author_role', 'quote')
    
    fieldsets = (
        ('Author Information', {
            'fields': ('author_name', 'author_role', 'author_image')
        }),
        ('Testimonial Content', {
            'fields': ('quote',)
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'order')
        }),
    )


# =========================================================================
# RESOURCES ADMIN INTERFACES
# =========================================================================

@admin.register(ResourcesConfiguration)
class ResourcesConfigurationAdmin(admin.ModelAdmin):
    """Admin for Resources page configuration."""
    
    def has_add_permission(self, request):
        """Prevent creating multiple instances."""
        return not ResourcesConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the configuration."""
        return False
    
    fieldsets = (
        ('Page Header', {
            'fields': ('page_title', 'intro_paragraph')
        }),
        ('Content Settings', {
            'fields': ('resources_description', 'resources_per_page')
        }),
    )


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    """Admin for resource categories."""
    list_display = ('name', 'slug', 'order', 'description')
    list_editable = ('order',)
    search_fields = ('name', 'description')
    ordering = ('order', 'name')
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'description', 'icon')
        }),
        ('Display Settings', {
            'fields': ('order',)
        }),
    )


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """Admin for resources with comprehensive management features."""
    list_display = (
        'title', 'resource_type', 'author', 'personal_rating', 
        'is_featured', 'is_active', 'created_date'
    )
    list_filter = (
        'resource_type', 'is_featured', 'is_active', 'personal_rating',
        'categories', 'created_date'
    )
    search_fields = ('title', 'description', 'author')
    filter_horizontal = ('categories', 'technologies')
    list_editable = ('is_featured', 'is_active', 'personal_rating')
    date_hierarchy = 'created_date'
    ordering = ('order', '-created_date')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'resource_type')
        }),
        ('Resource Content', {
            'fields': ('link', 'file_upload')
        }),
        ('Video Embedding', {
            'fields': ('youtube_embed_id', 'vimeo_embed_id', 'custom_embed_code'),
            'classes': ('collapse',),
            'description': 'For video resources, provide embed information'
        }),
        ('Visual Content', {
            'fields': ('thumbnail', 'preview_image'),
            'classes': ('collapse',)
        }),
        ('Categorization', {
            'fields': ('categories', 'technologies'),
        }),
        ('Metadata', {
            'fields': ('author', 'publication_date'),
            'classes': ('collapse',)
        }),
        ('Management', {
            'fields': ('is_featured', 'is_active', 'order', 'personal_rating')
        }),
    )
    
    # Custom actions
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_as_featured.short_description = "Mark selected resources as featured"
    
    def mark_as_unfeatured(self, request, queryset):
        queryset.update(is_featured=False)
    mark_as_unfeatured.short_description = "Remove featured status"
    
    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_as_active.short_description = "Mark selected resources as active"
    
    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_as_inactive.short_description = "Mark selected resources as inactive"
    
    actions = ['mark_as_featured', 'mark_as_unfeatured', 'mark_as_active', 'mark_as_inactive']


@admin.register(ResourceView)
class ResourceViewAdmin(admin.ModelAdmin):
    """Admin for resource view analytics."""
    list_display = ('resource', 'viewed_date', 'ip_address')
    list_filter = ('viewed_date', 'resource__resource_type')
    search_fields = ('resource__title', 'ip_address')
    date_hierarchy = 'viewed_date'
    ordering = ('-viewed_date',)
    
    # Make it read-only since this is analytics data
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False