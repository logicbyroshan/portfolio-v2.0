from django.contrib import admin
from .models import Blog, Comment, CommentLike


# =========================================================================
# INLINES
# =========================================================================

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('author_name', 'body', 'is_approved', 'created_date')
    readonly_fields = ('created_date',)


# =========================================================================
# ADMIN CLASSES
# =========================================================================

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


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('user__username', 'comment__post__title')
    
    # Make it read-only since this is user interaction data
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
