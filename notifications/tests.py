from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch, Mock, MagicMock
from portfolio.models import ContactSubmission
from notifications.models import ContactNotification, NotificationSettings
from notifications.services import PushNotificationService
import json


class SignalHandlerTests(TestCase):
    """Test cases for contact submission signal handler"""

    def setUp(self):
        """Set up test fixtures"""
        # Create notification settings with push enabled
        self.settings = NotificationSettings.objects.create(
            id=1,
            admin_email='admin@test.com',
            push_notification_enabled=True,
            fcm_server_key='test_server_key',
            fcm_device_token='test_device_token'
        )

    @patch('notifications.services.PushNotificationService.send_priority_notification')
    @patch('notifications.services.EmailNotificationService.send_thankyou_notification')
    @patch('notifications.services.EmailNotificationService.send_admin_notification')
    def test_signal_triggers_push_for_urgent_message(self, mock_admin_email, mock_thankyou_email, mock_push):
        """Test that creating urgent contact triggers push notification"""
        # Mock all notification methods to return success
        mock_admin_email.return_value = True
        mock_thankyou_email.return_value = True
        mock_push.return_value = True
        
        # Create an urgent contact submission (this should trigger the signal)
        contact = ContactSubmission.objects.create(
            name='Urgent User',
            email='urgent@test.com',
            subject='Urgent Request',
            message='This is urgent!',
            is_urgent=True
        )
        
        # Verify push notification method was called
        mock_push.assert_called_once()
        
        # Verify the contact submission and notification were passed correctly
        call_args = mock_push.call_args[0]
        self.assertEqual(call_args[0].id, contact.id)
        self.assertEqual(call_args[0].is_urgent, True)

    @patch('notifications.services.PushNotificationService.send_priority_notification')
    @patch('notifications.services.EmailNotificationService.send_thankyou_notification')
    @patch('notifications.services.EmailNotificationService.send_admin_notification')
    def test_signal_skips_push_for_normal_message(self, mock_admin_email, mock_thankyou_email, mock_push):
        """Test that creating normal contact does not trigger push notification"""
        # Mock email methods to return success
        mock_admin_email.return_value = True
        mock_thankyou_email.return_value = True
        
        # Create a normal (non-urgent) contact submission
        contact = ContactSubmission.objects.create(
            name='Normal User',
            email='normal@test.com',
            subject='Regular Question',
            message='Just a question',
            is_urgent=False
        )
        
        # Verify push notification method was NOT called
        mock_push.assert_not_called()

    @patch('notifications.services.EmailNotificationService.send_thankyou_notification')
    @patch('notifications.services.EmailNotificationService.send_admin_notification')
    def test_notification_record_created_on_contact_submission(self, mock_admin_email, mock_thankyou_email):
        """Test that ContactNotification record is created when contact is submitted"""
        mock_admin_email.return_value = True
        mock_thankyou_email.return_value = True
        
        # Create a contact submission
        contact = ContactSubmission.objects.create(
            name='Test User',
            email='test@test.com',
            subject='Test',
            message='Test message',
            is_urgent=True
        )
        
        # Verify notification record was created
        self.assertTrue(
            ContactNotification.objects.filter(contact_submission=contact).exists()
        )
        
        notification = ContactNotification.objects.get(contact_submission=contact)
        self.assertEqual(notification.status, ContactNotification.NotificationStatus.PENDING)


class PushNotificationServiceTests(TestCase):
    """Test cases for Push Notification Service"""

    def setUp(self):
        """Set up test fixtures"""
        # Create notification settings
        self.settings = NotificationSettings.objects.create(
            id=1,
            admin_email='admin@test.com',
            push_notification_enabled=True,
            fcm_server_key='test_server_key',
            fcm_device_token='test_device_token'
        )
        
        # Create a test contact submission (urgent)
        self.urgent_contact = ContactSubmission.objects.create(
            name='John Urgent',
            email='urgent@test.com',
            subject='Urgent Matter',
            message='This is an urgent message requiring immediate attention.',
            is_urgent=True
        )
        
        # Create a test contact submission (non-urgent)
        self.normal_contact = ContactSubmission.objects.create(
            name='Jane Normal',
            email='normal@test.com',
            subject='Regular Inquiry',
            message='This is a regular message.',
            is_urgent=False
        )
        
        # Create notification records
        self.urgent_notification = ContactNotification.objects.create(
            contact_submission=self.urgent_contact,
            status=ContactNotification.NotificationStatus.PENDING
        )
        
        self.normal_notification = ContactNotification.objects.create(
            contact_submission=self.normal_contact,
            status=ContactNotification.NotificationStatus.PENDING
        )
        
        self.push_service = PushNotificationService()

    def test_push_notification_service_initialization(self):
        """Test that PushNotificationService initializes correctly"""
        self.assertIsNotNone(self.push_service.settings)
        self.assertEqual(self.push_service.fcm_url, "https://fcm.googleapis.com/fcm/send")

    def test_skip_push_for_non_urgent_message(self):
        """Test that push notification is skipped for non-urgent messages"""
        result = self.push_service.send_priority_notification(
            self.normal_contact,
            self.normal_notification
        )
        
        self.assertFalse(result)
        # Verify notification tracking wasn't updated
        self.normal_notification.refresh_from_db()
        self.assertFalse(self.normal_notification.push_notification_sent)

    def test_skip_push_when_disabled_in_settings(self):
        """Test that push notification is skipped when disabled in settings"""
        self.settings.push_notification_enabled = False
        self.settings.save()
        
        result = self.push_service.send_priority_notification(
            self.urgent_contact,
            self.urgent_notification
        )
        
        self.assertFalse(result)

    def test_skip_push_when_fcm_server_key_missing(self):
        """Test that push notification is skipped when FCM server key is missing"""
        self.settings.fcm_server_key = ''
        self.settings.save()
        
        result = self.push_service.send_priority_notification(
            self.urgent_contact,
            self.urgent_notification
        )
        
        self.assertFalse(result)

    def test_skip_push_when_fcm_device_token_missing(self):
        """Test that push notification is skipped when FCM device token is missing"""
        self.settings.fcm_device_token = ''
        self.settings.save()
        
        result = self.push_service.send_priority_notification(
            self.urgent_contact,
            self.urgent_notification
        )
        
        self.assertFalse(result)

    @patch('notifications.services.requests.post')
    def test_successful_push_notification(self, mock_post):
        """Test successful push notification delivery"""
        # Mock successful FCM response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': 1,
            'failure': 0,
            'results': [{'message_id': '0:1234567890'}]
        }
        mock_post.return_value = mock_response
        
        result = self.push_service.send_priority_notification(
            self.urgent_contact,
            self.urgent_notification
        )
        
        self.assertTrue(result)
        
        # Verify FCM API was called correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        # Check URL
        self.assertEqual(call_args[0][0], "https://fcm.googleapis.com/fcm/send")
        
        # Check headers
        headers = call_args[1]['headers']
        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertEqual(headers['Authorization'], 'key=test_server_key')
        
        # Check payload
        payload = json.loads(call_args[1]['data'])
        self.assertEqual(payload['to'], 'test_device_token')
        self.assertEqual(payload['priority'], 'high')
        self.assertIn('Priority Message Received', payload['notification']['title'])
        self.assertIn('John Urgent', payload['notification']['body'])
        
        # Verify notification tracking was updated
        self.urgent_notification.refresh_from_db()
        self.assertTrue(self.urgent_notification.push_notification_sent)
        self.assertIsNotNone(self.urgent_notification.push_notification_sent_at)
        self.assertIsNone(self.urgent_notification.push_notification_error)

    @patch('notifications.services.requests.post')
    def test_failed_push_notification_fcm_error(self, mock_post):
        """Test failed push notification due to FCM error"""
        # Mock FCM error response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': 0,
            'failure': 1,
            'results': [{'error': 'InvalidRegistration'}]
        }
        mock_post.return_value = mock_response
        
        result = self.push_service.send_priority_notification(
            self.urgent_contact,
            self.urgent_notification
        )
        
        self.assertFalse(result)
        
        # Verify notification tracking records the error
        self.urgent_notification.refresh_from_db()
        self.assertFalse(self.urgent_notification.push_notification_sent)
        self.assertIsNotNone(self.urgent_notification.push_notification_error)
        self.assertIn('InvalidRegistration', self.urgent_notification.push_notification_error)

    @patch('notifications.services.requests.post')
    def test_failed_push_notification_http_error(self, mock_post):
        """Test failed push notification due to HTTP error"""
        # Mock HTTP error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = 'Unauthorized'
        mock_post.return_value = mock_response
        
        result = self.push_service.send_priority_notification(
            self.urgent_contact,
            self.urgent_notification
        )
        
        self.assertFalse(result)
        
        # Verify notification tracking records the error
        self.urgent_notification.refresh_from_db()
        self.assertFalse(self.urgent_notification.push_notification_sent)
        self.assertIsNotNone(self.urgent_notification.push_notification_error)

    @patch('notifications.services.requests.post')
    def test_push_notification_network_error(self, mock_post):
        """Test push notification handling of network errors"""
        # Mock network error
        mock_post.side_effect = Exception("Network timeout")
        
        result = self.push_service.send_priority_notification(
            self.urgent_contact,
            self.urgent_notification
        )
        
        self.assertFalse(result)
        
        # Verify error was tracked
        self.urgent_notification.refresh_from_db()
        self.assertFalse(self.urgent_notification.push_notification_sent)
        self.assertIsNotNone(self.urgent_notification.push_notification_error)

    @patch('notifications.services.requests.post')
    def test_push_notification_payload_structure(self, mock_post):
        """Test that push notification payload has correct structure"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': 1, 'results': [{}]}
        mock_post.return_value = mock_response
        
        self.push_service.send_priority_notification(
            self.urgent_contact,
            self.urgent_notification
        )
        
        # Extract the payload from the mock call
        call_args = mock_post.call_args
        payload = json.loads(call_args[1]['data'])
        
        # Verify payload structure
        self.assertIn('to', payload)
        self.assertIn('priority', payload)
        self.assertIn('notification', payload)
        self.assertIn('data', payload)
        
        # Verify notification data
        notification = payload['notification']
        self.assertIn('title', notification)
        self.assertIn('body', notification)
        self.assertIn('sound', notification)
        
        # Verify custom data
        data = payload['data']
        self.assertEqual(data['contact_id'], str(self.urgent_contact.id))
        self.assertEqual(data['sender_name'], 'John Urgent')
        self.assertEqual(data['sender_email'], 'urgent@test.com')
        self.assertEqual(data['is_urgent'], 'true')
        self.assertEqual(data['type'], 'priority_contact')


class ContactNotificationModelTests(TestCase):
    """Test cases for ContactNotification model methods"""

    def setUp(self):
        """Set up test fixtures"""
        self.contact = ContactSubmission.objects.create(
            name='Test User',
            email='test@example.com',
            subject='Test Subject',
            message='Test message',
            is_urgent=True
        )
        
        self.notification = ContactNotification.objects.create(
            contact_submission=self.contact,
            status=ContactNotification.NotificationStatus.PENDING
        )

    def test_mark_push_notification_sent_success(self):
        """Test marking push notification as successfully sent"""
        self.notification.mark_push_notification_sent()
        
        self.assertTrue(self.notification.push_notification_sent)
        self.assertIsNotNone(self.notification.push_notification_sent_at)
        self.assertIsNone(self.notification.push_notification_error)

    def test_mark_push_notification_sent_with_error(self):
        """Test marking push notification as failed with error"""
        error_message = "FCM authentication failed"
        self.notification.mark_push_notification_sent(error=error_message)
        
        self.assertFalse(self.notification.push_notification_sent)
        self.assertIsNotNone(self.notification.push_notification_sent_at)
        self.assertEqual(self.notification.push_notification_error, error_message)


class NotificationSettingsModelTests(TestCase):
    """Test cases for NotificationSettings model"""

    def test_singleton_pattern(self):
        """Test that only one NotificationSettings instance can exist"""
        settings1 = NotificationSettings.objects.create(
            id=1,
            admin_email='admin1@test.com',
            push_notification_enabled=True
        )
        
        settings2 = NotificationSettings.objects.create(
            admin_email='admin2@test.com',
            push_notification_enabled=False
        )
        
        # Should still only have one instance
        self.assertEqual(NotificationSettings.objects.count(), 1)
        
        # The first instance should be updated with second's values
        settings1.refresh_from_db()
        self.assertEqual(settings1.admin_email, 'admin2@test.com')
        self.assertFalse(settings1.push_notification_enabled)

    def test_get_settings_creates_default(self):
        """Test that get_settings creates default settings if none exist"""
        self.assertEqual(NotificationSettings.objects.count(), 0)
        
        settings = NotificationSettings.get_settings()
        
        self.assertIsNotNone(settings)
        self.assertEqual(NotificationSettings.objects.count(), 1)
        self.assertEqual(settings.admin_email, 'contact@roshandamor.me')

    def test_push_notification_fields_defaults(self):
        """Test default values for push notification fields"""
        settings = NotificationSettings.objects.create(id=1)
        
        self.assertFalse(settings.push_notification_enabled)
        self.assertEqual(settings.fcm_server_key, '')
        self.assertEqual(settings.fcm_device_token, '')

