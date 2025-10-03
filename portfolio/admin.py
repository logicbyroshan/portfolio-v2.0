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
    SkillTechnologyDetail,
    Achievement,
    Resume,
    VideoResume,
    NewsletterSubscriber,
    ContactSubmission,
    CodeTogetherConfiguration,
    CollaborationProposal,
    Testimonial,
)

# =========================================================================
# MODEL ADMINS
# =========================================================================


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    """Admin for the Site Configuration object."""

    fieldsets = (
        ("Hero Section", {"fields": ("hero_greeting", "hero_name", "hero_tagline")}),
        (
            "Hero Stats",
            {
                "fields": (
                    "hero_projects_stat",
                    "hero_internships_stat",
                    "hero_articles_stat",
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


class SkillTechnologyDetailInline(admin.TabularInline):
    model = SkillTechnologyDetail
    extra = 1


# =========================================================================
# REGULAR MODEL ADMIN CONFIGURATIONS
# =========================================================================


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category_type")
    list_filter = ("category_type",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = ("title", "created_date")
    list_filter = ("categories", "technologies")
    search_fields = ("title", "summary")
    filter_horizontal = ("technologies", "categories")


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
    inlines = [SkillTechnologyDetailInline]
    list_display = ("title", "icon")
    search_fields = ("title", "summary")


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


@admin.register(CodeTogetherConfiguration)
class CodeTogetherConfigurationAdmin(admin.ModelAdmin):
    """Admin for the Code Together Configuration object."""

    fieldsets = (
        ("Page Header", {"fields": ("page_title", "intro_paragraph")}),
        ("Interests Section", {"fields": ("interests_content",)}),
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

    list_display = ("full_name", "email", "status", "submitted_date", "reviewed_date")
    list_filter = ("status", "submitted_date")
    search_fields = ("full_name", "email", "github_id", "linkedin_id")
    readonly_fields = ("submitted_date",)

    fieldsets = (
        (
            "Proposal Information",
            {"fields": ("full_name", "email", "github_id", "linkedin_id", "proposal")},
        ),
        (
            "Status & Management",
            {"fields": ("status", "submitted_date", "reviewed_date", "admin_notes")},
        ),
    )

    def mark_as_reviewing(self, request, queryset):
        queryset.update(status="reviewing")

    def mark_as_accepted(self, request, queryset):
        queryset.update(status="accepted")

    def mark_as_declined(self, request, queryset):
        queryset.update(status="declined")

    actions = ["mark_as_reviewing", "mark_as_accepted", "mark_as_declined"]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin for testimonials."""

    list_display = (
        "author_name",
        "author_role",
        "is_featured",
        "order",
        "created_date",
    )
    list_filter = ("is_featured", "created_date")
    search_fields = ("author_name", "author_role", "quote")

    fieldsets = (
        (
            "Author Information",
            {"fields": ("author_name", "author_role", "author_image")},
        ),
        ("Testimonial Content", {"fields": ("quote",)}),
        ("Display Settings", {"fields": ("is_featured", "order")}),
    )
