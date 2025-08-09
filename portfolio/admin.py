from django.contrib import admin
from .models import (
    Technology, Category, Project, ProjectImage, Blog, Comment, 
    Experience, FAQ, Skill, SkillTechnologyDetail
)

# =========================================================================
# INLINES - For managing related models within a parent's admin page
# =========================================================================

class ProjectImageInline(admin.TabularInline):
    """Allows adding multiple project images directly within the Project admin page."""
    model = ProjectImage
    extra = 1  # Number of empty forms to display
    verbose_name = "Project Image"
    verbose_name_plural = "Project Images (for slider)"

class CommentInline(admin.TabularInline):
    """Allows managing comments directly within the Blog admin page."""
    model = Comment
    extra = 0
    fields = ('author_name', 'body', 'is_approved', 'created_date')
    readonly_fields = ('created_date',)

class SkillTechnologyDetailInline(admin.TabularInline):
    """Allows defining technology details directly within the Skill admin page."""
    model = SkillTechnologyDetail
    extra = 1
    verbose_name = "Technology Detail"
    verbose_name_plural = "Technology Details"


# =========================================================================
# MODEL ADMIN CONFIGURATIONS
# =========================================================================

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    # Slug is auto-generated, so no need for prepopulated_fields here

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = ('title', 'created_date')
    list_filter = ('categories', 'technologies')
    search_fields = ('title', 'summary', 'content')
    filter_horizontal = ('technologies', 'categories') # Better UX for ManyToMany
    # Slug is auto-generated

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('title', 'author_name', 'created_date')
    list_filter = ('categories', 'created_date')
    search_fields = ('title', 'summary', 'content')
    filter_horizontal = ('categories',)
    # Slug is auto-generated

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
    list_display = ('role', 'company_name', 'start_date', 'end_date', 'experience_type')
    list_filter = ('experience_type', 'technologies')
    search_fields = ('role', 'company_name', 'summary')
    filter_horizontal = ('technologies',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    inlines = [SkillTechnologyDetailInline]
    list_display = ('title', 'icon')
    search_fields = ('title', 'summary')
    # Slug is auto-generated