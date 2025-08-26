# ai/models.py
from django.db import models

class AIQuery(models.Model):
    question = models.TextField()
    attachment = models.FileField(upload_to='query_attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query from {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name_plural = "AI Queries"
        ordering = ['-created_at']