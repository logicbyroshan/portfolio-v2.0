import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import (
    SiteConfiguration,
    Technology,
    Category,
    Project,
    ProjectImage,
    Experience,
    FAQ,
    Skill,
    Achievement,
    Resume,
    VideoResume,
    NewsletterSubscriber,
    ContactSubmission,
)

# =========================================================================
# MODEL ADMINS
# =========================================================================


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    """Admin for the Site Configuration object."""

    fieldsets = (
        ("Hero Section", {"fields": ("hero_name",)}),
        (
            "Hero Stats",
            {
                "fields": (
                    "hero_leetcode_rating",
                    "hero_opensource_contributions",
                    "hero_hackathons_count",
                )
            },
        ),
        (
            "Social Media Links",
            {
                "fields": (
                    "twitter_url",
                    "github_url",
                    "linkedin_url",
                    "youtube_url",
                    "instagram_url",
                    "facebook_url",
                )
            },
        ),
        ("Contact Information", {"fields": ("email", "phone", "location")}),
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


# =========================================================================
# REGULAR MODEL ADMIN CONFIGURATIONS
# =========================================================================


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "category")
    list_filter = ("category",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category_type")
    list_filter = ("category_type",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = ("title", "created_date", "has_youtube_video")
    list_filter = ("categories", "technologies")
    search_fields = ("title", "summary")
    filter_horizontal = ("technologies", "categories")
    fieldsets = (
        ("Basic Information", {"fields": ("title", "summary", "content")}),
        ("Media", {"fields": ("cover_image", "youtube_url")}),
        ("Categorization", {"fields": ("technologies", "categories")}),
        ("Links", {"fields": ("github_url", "live_url")}),
    )

    def has_youtube_video(self, obj):
        return bool(obj.youtube_url)

    has_youtube_video.boolean = True
    has_youtube_video.short_description = "Has Video"


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company_name", "start_date", "end_date")
    list_filter = ("experience_type",)
    search_fields = ("role", "company_name")
    filter_horizontal = ("technologies",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order")
    list_editable = ("order",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "proficiency_level",
        "years_of_experience",
        "is_featured",
        "order",
    )
    list_filter = ("category", "proficiency_level", "is_featured")
    search_fields = ("title",)
    filter_horizontal = ("technologies",)
    list_editable = ("order", "is_featured", "category")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_date")
    search_fields = ("email",)
    actions = ["export_as_csv"]

    @admin.action(description="Export selected subscribers as CSV")
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta}.csv"
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "submitted_date", "is_read")
    list_filter = ("is_read",)
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "submitted_date")
    actions = ["mark_as_read"]

    @admin.action(description="Mark selected submissions as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("title", "issuing_organization", "category", "date_issued")
    list_filter = ("category", "date_issued")
    search_fields = ("title", "issuing_organization", "summary")
