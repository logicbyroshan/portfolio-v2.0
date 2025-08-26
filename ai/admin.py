# ai/admin.py
from django.contrib import admin
from .models import AIQuery

@admin.register(AIQuery)
class AIQueryAdmin(admin.ModelAdmin):
    list_display = ('question', 'has_attachment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('question',)

    def has_attachment(self, obj):
        return bool(obj.attachment)
    has_attachment.boolean = True