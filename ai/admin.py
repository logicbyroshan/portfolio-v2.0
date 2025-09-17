# ai/admin.py
from django.contrib import admin
from .models import AIQuery, AIContext

@admin.register(AIQuery)
class AIQueryAdmin(admin.ModelAdmin):
    list_display = ('question', 'has_attachment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('question',)
    readonly_fields = ('created_at',)

    def has_attachment(self, obj):
        return bool(obj.attachment)
    has_attachment.boolean = True

@admin.register(AIContext)
class AIContextAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_active',)
    ordering = ['title']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'is_active')
        }),
        ('Content', {
            'fields': ('content',),
            'description': 'Add supporting content about Roshan Damor - personal background, work approach, philosophy, etc.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()