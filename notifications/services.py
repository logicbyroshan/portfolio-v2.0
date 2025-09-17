from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from .models import NotificationSettings, EmailTemplate
import logging

logger = logging.getLogger(__name__)

class EmailNotificationService:
    """
    Service class to handle email notifications for contact submissions
    """
    
    def __init__(self):
        self.settings = NotificationSettings.get_settings()
    
    def send_admin_notification(self, contact_submission, notification):
        """
        Send notification email to admin about new contact submission
        """
        if not self.settings.admin_notification_enabled:
            logger.info("Admin notifications are disabled")
            return False
        
        try:
            # Get email template or use default
            template = self._get_template('admin_notification')
            
            if template:
                subject = template.subject
                html_content = template.html_content
                text_content = template.text_content
            else:
                # Default template
                subject = f"New Contact Form Submission from {contact_submission.name}"
                html_content = self._get_default_admin_html_template()
                text_content = self._get_default_admin_text_template()
            
            # Prepare template context
            context = {
                'contact_name': contact_submission.name,
                'contact_email': contact_submission.email,
                'contact_subject': contact_submission.subject or 'No subject provided',
                'contact_message': contact_submission.message,
                'submission_date': contact_submission.submitted_date,
                'site_name': getattr(settings, 'SITE_NAME', 'Portfolio Website'),
                'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
            }
            
            # Render templates with context
            rendered_html = self._render_template_string(html_content, context)
            rendered_text = self._render_template_string(text_content, context)
            rendered_subject = self._render_template_string(subject, context)
            
            # Send email
            from django.core.mail import EmailMultiAlternatives
            email = EmailMultiAlternatives(
                subject=rendered_subject,
                body=rendered_text,
                from_email=self.settings.from_email,
                to=[self.settings.admin_email],
            )
            email.attach_alternative(rendered_html, "text/html")
            email.send(fail_silently=False)
            
            notification.mark_admin_email_sent()
            logger.info(f"Admin notification sent for contact submission {contact_submission.id}")
            return True
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to send admin notification: {error_msg}")
            try:
                notification.mark_admin_email_sent(error=error_msg)
            except Exception as inner_e:
                logger.error(f"Failed to mark admin email as failed: {str(inner_e)}")
            return False
    
    def send_thankyou_notification(self, contact_submission, notification):
        """
        Send thank you email to user who submitted contact form
        """
        if not self.settings.thankyou_notification_enabled:
            logger.info("Thank you notifications are disabled")
            return False
        
        try:
            # Get email template or use default
            template = self._get_template('user_thankyou')
            
            if template:
                subject = template.subject
                html_content = template.html_content
                text_content = template.text_content
            else:
                # Default template
                subject = "Thank you for contacting us!"
                html_content = self._get_default_thankyou_html_template()
                text_content = self._get_default_thankyou_text_template()
            
            # Prepare template context
            context = {
                'user_name': contact_submission.name,
                'user_email': contact_submission.email,
                'contact_subject': contact_submission.subject or 'your inquiry',
                'submission_date': contact_submission.submitted_date,
                'site_name': getattr(settings, 'SITE_NAME', 'Roshan Damor Portfolio'),
                'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
                'admin_name': 'Roshan Damor',
                'reply_email': self.settings.reply_to_email,
            }
            
            # Render templates with context
            rendered_html = self._render_template_string(html_content, context)
            rendered_text = self._render_template_string(text_content, context)
            rendered_subject = self._render_template_string(subject, context)
            
            # Send email
            from django.core.mail import EmailMultiAlternatives
            email = EmailMultiAlternatives(
                subject=rendered_subject,
                body=rendered_text,
                from_email=self.settings.from_email,
                to=[contact_submission.email],
                reply_to=[self.settings.reply_to_email],
            )
            email.attach_alternative(rendered_html, "text/html")
            email.send(fail_silently=False)
            
            notification.mark_thankyou_email_sent()
            logger.info(f"Thank you notification sent for contact submission {contact_submission.id}")
            return True
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to send thank you notification: {error_msg}")
            try:
                notification.mark_thankyou_email_sent(error=error_msg)
            except Exception as inner_e:
                logger.error(f"Failed to mark thankyou email as failed: {str(inner_e)}")
            return False
    
    def _get_template(self, template_type):
        """Get active email template by type"""
        try:
            return EmailTemplate.objects.filter(
                template_type=template_type,
                is_active=True
            ).first()
        except EmailTemplate.DoesNotExist:
            return None
    
    def _render_template_string(self, template_string, context):
        """Render template string with context variables"""
        try:
            from django.template import Template, Context
            template = Template(template_string)
            return template.render(Context(context))
        except Exception as e:
            logger.error(f"Template rendering error: {str(e)}")
            # Return template with basic string replacement as fallback
            result = template_string
            for key, value in context.items():
                result = result.replace(f'{{{{ {key} }}}}', str(value))
                # Also handle with spaces around variable name
                result = result.replace(f'{{{{  {key}  }}}}', str(value))
            return result
    
    def _get_default_admin_html_template(self):
        """Default HTML template for admin notification"""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>New Contact Form Submission</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
                .container { max-width: 600px; margin: 0 auto; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
                .content { padding: 30px; }
                .field { margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; border-left: 4px solid #667eea; }
                .field-label { font-weight: 600; color: #333; margin-bottom: 5px; }
                .field-value { color: #666; line-height: 1.5; }
                .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 14px; color: #666; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>New Contact Form Submission</h1>
                    <p>You have received a new message from your portfolio website</p>
                </div>
                <div class="content">
                    <div class="field">
                        <div class="field-label">From:</div>
                        <div class="field-value">{{ contact_name }} ({{ contact_email }})</div>
                    </div>
                    <div class="field">
                        <div class="field-label">Subject:</div>
                        <div class="field-value">{{ contact_subject }}</div>
                    </div>
                    <div class="field">
                        <div class="field-label">Message:</div>
                        <div class="field-value" style="white-space: pre-line;">{{ contact_message }}</div>
                    </div>
                    <div class="field">
                        <div class="field-label">Submitted:</div>
                        <div class="field-value">{{ submission_date }}</div>
                    </div>
                </div>
                <div class="footer">
                    <p>This email was sent from {{ site_name }}</p>
                    <p><a href="{{ site_url }}">Visit Website</a></p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_default_admin_text_template(self):
        """Default text template for admin notification"""
        return """
        NEW CONTACT FORM SUBMISSION
        
        From: {{ contact_name }} ({{ contact_email }})
        Subject: {{ contact_subject }}
        Submitted: {{ submission_date }}
        
        Message:
        {{ contact_message }}
        
        ---
        This email was sent from {{ site_name }}
        {{ site_url }}
        """
    
    def _get_default_thankyou_html_template(self):
        """Default HTML template for thank you email"""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Thank You for Contacting Us</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
                .container { max-width: 600px; margin: 0 auto; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
                .content { padding: 30px; line-height: 1.6; color: #333; }
                .highlight { background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #667eea; margin: 20px 0; }
                .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 14px; color: #666; }
                .button { display: inline-block; background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 10px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Thank You for Contacting Us!</h1>
                    <p>We've received your message and will get back to you soon</p>
                </div>
                <div class="content">
                    <p>Hi {{ user_name }},</p>
                    
                    <p>Thank you for reaching out through our contact form. We have successfully received your message regarding "{{ contact_subject }}" and appreciate you taking the time to contact us.</p>
                    
                    <div class="highlight">
                        <strong>What happens next?</strong><br>
                        • Your message has been forwarded to our team<br>
                        • We typically respond within 24-48 hours<br>
                        • You'll receive a reply at {{ user_email }}<br>
                        • For urgent matters, feel free to reach out directly
                    </div>
                    
                    <p>In the meantime, feel free to explore our website and check out our latest projects and blog posts.</p>
                    
                    <p style="text-align: center;">
                        <a href="{{ site_url }}" class="button">Visit Our Website</a>
                    </p>
                    
                    <p>Best regards,<br>
                    <strong>{{ admin_name }}</strong><br>
                    {{ site_name }}</p>
                </div>
                <div class="footer">
                    <p>This is an automated message. Please do not reply to this email.</p>
                    <p>For direct communication, reach us at: <a href="mailto:{{ reply_email }}">{{ reply_email }}</a></p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_default_thankyou_text_template(self):
        """Default text template for thank you email"""
        return """
        Thank You for Contacting Us!
        
        Hi {{ user_name }},
        
        Thank you for reaching out through our contact form. We have successfully received your message regarding "{{ contact_subject }}" and appreciate you taking the time to contact us.
        
        What happens next?
        • Your message has been forwarded to our team
        • We typically respond within 24-48 hours
        • You'll receive a reply at {{ user_email }}
        • For urgent matters, feel free to reach out directly
        
        In the meantime, feel free to explore our website and check out our latest projects and blog posts.
        
        Visit our website: {{ site_url }}
        
        Best regards,
        {{ admin_name }}
        {{ site_name }}
        
        ---
        This is an automated message. Please do not reply to this email.
        For direct communication, reach us at: {{ reply_email }}
        """