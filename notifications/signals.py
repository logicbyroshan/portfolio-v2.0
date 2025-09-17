from django.db.models.signals import post_save
from django.dispatch import receiver
from portfolio.models import ContactSubmission
from .models import ContactNotification
from .services import EmailNotificationService
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=ContactSubmission)
def handle_contact_submission(sender, instance, created, **kwargs):
    """
    Signal handler to automatically process new contact form submissions
    Creates notification record and triggers email notifications
    """
    if created:  # Only process newly created submissions
        try:
            # Create notification record
            notification = ContactNotification.objects.create(
                contact_submission=instance,
                status=ContactNotification.NotificationStatus.PENDING
            )
            
            logger.info(f"Created notification record for contact submission {instance.id}")
            
            # Initialize email service
            email_service = EmailNotificationService()
            
            # Send admin notification
            admin_success = email_service.send_admin_notification(instance, notification)
            
            # Send thank you notification to user
            thankyou_success = email_service.send_thankyou_notification(instance, notification)
            
            # Update notification status based on email results
            if admin_success and thankyou_success:
                notification.status = ContactNotification.NotificationStatus.COMPLETED
                notification.save()
                logger.info(f"Successfully processed all notifications for contact submission {instance.id}")
            elif admin_success:
                # At least admin was notified
                logger.warning(f"Admin notified but failed to send thank you email for submission {instance.id}")
            else:
                # Failed to send admin notification
                notification.status = ContactNotification.NotificationStatus.FAILED
                notification.save()
                logger.error(f"Failed to send admin notification for contact submission {instance.id}")
                
        except Exception as e:
            logger.error(f"Error processing contact submission {instance.id}: {str(e)}")
            # Try to update notification status if it exists
            try:
                notification = ContactNotification.objects.get(contact_submission=instance)
                notification.status = ContactNotification.NotificationStatus.FAILED
                notification.admin_email_error = str(e)
                notification.save()
            except ContactNotification.DoesNotExist:
                pass