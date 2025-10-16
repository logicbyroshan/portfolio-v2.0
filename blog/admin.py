from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Blog, Comment, CommentLike

# =========================================================================
# INLINES
# =========================================================================

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('author_name', 'body_preview', 'is_approved', 'created_date')
    readonly_fields = ('body_preview', 'created_date')
    
    def body_preview(self, obj):
        return obj.body[:100] + "..." if len(obj.body) > 100 else obj.body
    body_preview.short_description = "Comment Preview"

# =========================================================================
# ADMIN CLASSES
# =========================================================================

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = (
        'title', 
        'cover_preview',
        'reading_time_badge',
        'category_count',
        'comment_count', 
        'created_date'
    )
    list_filter = ('categories', 'created_date')
    search_fields = ('title', 'summary', 'content')
    filter_horizontal = ('categories',)
    readonly_fields = ('slug', 'reading_time', 'cover_preview')
    date_hierarchy = 'created_date'
    
    fieldsets = (
        ("📝 Content", {
            "fields": ("title", "slug", "summary", "content"),
            "classes": ("wide",)
        }),
        ("🖼️ Media", {
            "fields": ("cover_image", "cover_preview"),
            "classes": ("wide",)
        }),
        ("🏷️ Categorization", {
            "fields": ("categories",),
            "classes": ("wide",)
        }),
        ("📊 Metadata", {
            "fields": ("reading_time",),
            "classes": ("collapse",)
        }),
    )
    
    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 60px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">',
                obj.cover_image.url
            )
        return "No cover image"
    cover_preview.short_description = "Cover Preview"
    
    def reading_time_badge(self, obj):
        return format_html(
            '<span style="background: #17a2b8; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px;">{} min read</span>',
            obj.reading_time
        )
    reading_time_badge.short_description = "Reading Time"
    
    def category_count(self, obj):
        count = obj.categories.count()
        return format_html(
            '<span style="background: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{} cat{}</span>',
            count,
            "s" if count != 1 else ""
        )
    category_count.short_description = "Categories"
    
    def comment_count(self, obj):
        count = obj.comments.count()
        approved_count = obj.comments.filter(is_approved=True).count()
        return format_html(
            '<span style="background: #6f42c1; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}/{} comments</span>',
            approved_count,
            count
        )
    comment_count.short_description = "Comments"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author_name', 
        'post_title',
        'body_preview',
        'approval_status',
        'like_count',
        'created_date'
    )
    list_filter = ('is_approved', 'created_date', 'post')
    search_fields = ('author_name', 'body', 'post__title')
    actions = ['approve_comments', 'disapprove_comments']
    readonly_fields = ('created_date', 'like_count')
    date_hierarchy = 'created_date'
    
    fieldsets = (
        ("💬 Comment Details", {
            "fields": ("post", "author_name", "author_email", "body"),
            "classes": ("wide",)
        }),
        ("✅ Moderation", {
            "fields": ("is_approved",),
            "classes": ("wide",)
        }),
        ("📊 Stats", {
            "fields": ("created_date", "like_count"),
            "classes": ("collapse",)
        }),
    )
    
    def post_title(self, obj):
        return format_html(
            '<a href="{}" style="color: #007bff; text-decoration: none;">{}</a>',
            f"/admin/blog/blog/{obj.post.id}/change/",
            obj.post.title[:50] + "..." if len(obj.post.title) > 50 else obj.post.title
        )
    post_title.short_description = "Blog Post"
    
    def body_preview(self, obj):
        return obj.body[:100] + "..." if len(obj.body) > 100 else obj.body
    body_preview.short_description = "Comment"
    
    def approval_status(self, obj):
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            '#28a745' if obj.is_approved else '#dc3545',
            '✅ Approved' if obj.is_approved else '⏳ Pending'
        )
    approval_status.short_description = "Status"
    
    def like_count(self, obj):
        count = obj.likes.count()
        return format_html(
            '<span style="background: #e83e8c; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">❤️ {}</span>',
            count
        )
    like_count.short_description = "Likes"
    
    @admin.action(description='✅ Approve selected comments')
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comments were successfully approved.')
        
    @admin.action(description='❌ Disapprove selected comments')
    def disapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comments were disapproved.')

@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment_preview', 'post_title', 'created_date')
    list_filter = ('created_date', 'comment__post')
    search_fields = ('user__username', 'comment__post__title', 'comment__author_name')
    readonly_fields = ('user', 'comment', 'created_date')
    date_hierarchy = 'created_date'
    
    def comment_preview(self, obj):
        return obj.comment.body[:50] + "..." if len(obj.comment.body) > 50 else obj.comment.body
    comment_preview.short_description = "Comment"
    
    def post_title(self, obj):
        return obj.comment.post.title
    post_title.short_description = "Blog Post"
    
    # Make it read-only since this is user interaction data
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
