from django.core.management.base import BaseCommand
from django.conf import settings
from notifications.models import NotificationSettings
import os

class Command(BaseCommand):
    help = 'Set up initial notification settings for the portfolio'

    def handle(self, *args, **options):
        """Create or update notification settings"""
        
        self.stdout.write(self.style.SUCCESS('Setting up notification system...'))
        
        # Get or create notification settings
        settings_obj, created = NotificationSettings.objects.get_or_create(
            defaults={
                'admin_email': 'contact@roshandamor.me',
                'from_email': os.getenv('EMAIL_HOST_USER', 'noreply@roshandamor.me'),
                'reply_to_email': 'contact@roshandamor.me',
                'admin_notification_enabled': True,
                'thankyou_notification_enabled': True,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('✓ Created new notification settings')
            )
        else:
            self.stdout.write(
                self.style.WARNING('✓ Notification settings already exist')
            )
        
        # Display current settings
        self.stdout.write('\nCurrent Notification Settings:')
        self.stdout.write(f'  Admin Email: {settings_obj.admin_email}')
        self.stdout.write(f'  From Email: {settings_obj.from_email}')
        self.stdout.write(f'  Reply To Email: {settings_obj.reply_to_email}')
        self.stdout.write(f'  Admin Notifications: {"Enabled" if settings_obj.admin_notification_enabled else "Disabled"}')
        self.stdout.write(f'  Thank You Notifications: {"Enabled" if settings_obj.thankyou_notification_enabled else "Disabled"}')
        
        self.stdout.write(
            self.style.SUCCESS('\n✓ Notification system setup complete!')
        )
        
        return