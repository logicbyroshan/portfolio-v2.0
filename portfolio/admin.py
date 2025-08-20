import csv
from django.http import HttpResponse
from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import (
    SiteConfiguration, Technology, Category, Project, ProjectImage, Blog, Comment, 
    Experience, FAQ, Skill, SkillTechnologyDetail, Service, Achievement, NowItem,
    Resume, VideoResume, NewsletterSubscriber, ContactSubmission
)

# =========================================================================
# SINGLETON MODEL ADMINS
# =========================================================================

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonModelAdmin):
    """Admin for the single Site Configuration object."""
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_greeting', 'hero_name', 'hero_tagline', 'hero_bio')
        }),
        ('Hero Stats', {
            'fields': ('hero_projects_stat', 'hero_internships_stat', 'hero_articles_stat')
        }),
        ('Section Titles & Descriptions', {
            'classes': ('collapse',), # Collapsible section
            'fields': (
                'about_title', 'about_description', 'now_title', 'now_description',
                'skills_title', 'skills_description', 'experience_title', 'experience_description'
                # ... add other section titles here
            )
        }),
    )

@admin.register(Resume)
class ResumeAdmin(SingletonModelAdmin):
    pass

@admin.register(VideoResume)
class VideoResumeAdmin(SingletonModelAdmin):
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
    list_display = ('title', 'icon')
    search_fields = ('title',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(NowItem)
class NowItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

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