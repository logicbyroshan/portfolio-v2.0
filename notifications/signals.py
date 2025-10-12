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
    # 🔍 DEBUG: Log signal trigger
    print("=" * 70)
    print(f"🔔 NOTIFICATION SIGNAL HANDLER TRIGGERED")
    print(f"   Created (new submission): {created}")
    print(f"   Contact ID: {instance.id}")
    print(f"   Name: {instance.name}")
    print(f"   Email: {instance.email}")
    print(f"   Subject: {instance.subject}")
    print("=" * 70)

    if created:  # Only process newly created submissions
        try:
            # Create notification record
            notification = ContactNotification.objects.create(
                contact_submission=instance,
                status=ContactNotification.NotificationStatus.PENDING,
            )

            logger.info(
                f"Created notification record for contact submission {instance.id}"
            )
            print(f"✅ Created notification record: ID={notification.id}")

            # Initialize email service
            email_service = EmailNotificationService()
            print(f"📧 Initialized EmailNotificationService")

            # Send admin notification
            print(f"📤 Attempting to send admin notification...")
            admin_success = email_service.send_admin_notification(
                instance, notification
            )
            print(
                f"   Admin email result: {'✅ SUCCESS' if admin_success else '❌ FAILED'}"
            )

            # Send thank you notification to user
            print(f"📤 Attempting to send thank you email...")
            thankyou_success = email_service.send_thankyou_notification(
                instance, notification
            )
            print(
                f"   Thank you email result: {'✅ SUCCESS' if thankyou_success else '❌ FAILED'}"
            )

            # Update notification status based on email results
            if admin_success and thankyou_success:
                notification.status = ContactNotification.NotificationStatus.COMPLETED
                notification.save()
                logger.info(
                    f"Successfully processed all notifications for contact submission {instance.id}"
                )
                print(f"✅ All notifications completed successfully")
            elif admin_success:
                # At least admin was notified
                logger.warning(
                    f"Admin notified but failed to send thank you email for submission {instance.id}"
                )
                print(f"⚠️  Admin notified but thank you email failed")
            else:
                # Failed to send admin notification
                notification.status = ContactNotification.NotificationStatus.FAILED
                notification.save()
                logger.error(
                    f"Failed to send admin notification for contact submission {instance.id}"
                )
                print(f"❌ Failed to send admin notification")

            print("=" * 70)

        except Exception as e:
            logger.error(f"Error processing contact submission {instance.id}: {str(e)}")
            print(f"❌ ERROR in signal handler: {str(e)}")
            import traceback

            traceback.print_exc()
            print("=" * 70)
            # Try to update notification status if it exists
            try:
                notification = ContactNotification.objects.get(
                    contact_submission=instance
                )
                notification.status = ContactNotification.NotificationStatus.FAILED
                notification.admin_email_error = str(e)
                notification.save()
            except ContactNotification.DoesNotExist:
                pass
