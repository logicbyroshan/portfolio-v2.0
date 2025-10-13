# 📱 Push Notifications for Urgent Contact Messages

## Overview

This feature implements Firebase Cloud Messaging (FCM) based push notifications for urgent contact form submissions. When a visitor marks their message as "Urgent" in the contact form, the system automatically sends a push notification to the admin's smartphone, ensuring priority messages receive a response within 24 hours.

## Features

- ✅ **Instant Notifications** - Push alerts sent immediately when urgent messages are received
- ✅ **Rich Notification Data** - Includes sender name, email, subject, and message snippet
- ✅ **Conditional Triggering** - Only urgent messages trigger push notifications
- ✅ **Configurable** - Enable/disable push notifications via Django admin
- ✅ **Error Tracking** - Failed notifications are logged with error details
- ✅ **Email Integration** - Works alongside existing email notification system

## Architecture

### Components

1. **NotificationSettings Model** - Stores FCM configuration (server key, device token)
2. **ContactNotification Model** - Tracks push notification delivery status
3. **PushNotificationService** - Handles FCM API communication
4. **Signal Handler** - Automatically triggers notifications on new urgent contacts
5. **Admin Interface** - Configure settings and view notification history

### Workflow

```
User submits urgent message
        ↓
Signal handler triggered (post_save)
        ↓
Check if is_urgent = True
        ↓
PushNotificationService.send_priority_notification()
        ↓
Send POST request to FCM API
        ↓
Update ContactNotification record
        ↓
Admin receives push notification on smartphone
```

## Setup Instructions

### 1. Firebase Project Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select an existing one
3. Navigate to **Project Settings** → **Cloud Messaging**
4. Copy the **Server Key** (Legacy)

### 2. Mobile App Setup

You need a mobile app with FCM integration to receive push notifications:

**Option A: Use existing FCM-enabled app**
- Install any FCM-compatible app on your smartphone
- Get the device registration token from the app

**Option B: Create custom app (recommended)**
- Create a simple Android/iOS app using Flutter, React Native, or native code
- Integrate Firebase Cloud Messaging SDK
- Register for push notifications and obtain the device token

**Option C: Use a third-party service**
- Consider services like OneSignal or Pushover as alternatives to FCM
- Update the `PushNotificationService` to use their APIs

### 3. Environment Configuration

Add these variables to your `.env` file:

```bash
# Firebase Cloud Messaging
FCM_SERVER_KEY=your_firebase_cloud_messaging_server_key
FCM_DEVICE_TOKEN=your_fcm_device_token_from_mobile_app
```

### 4. Django Admin Configuration

1. Log in to Django Admin
2. Navigate to **Notification Settings**
3. Enable **Push Notification Enabled**
4. Enter your **FCM Server Key**
5. Enter your **FCM Device Token**
6. Save settings

### 5. Database Migration

Run migrations to add push notification fields:

```bash
python manage.py migrate notifications
```

## Testing

### Run Unit Tests

```bash
python manage.py test notifications.tests.PushNotificationServiceTests
python manage.py test notifications.tests.SignalHandlerTests
```

### Manual Testing

1. **Test with Mock FCM**: Use the test cases to verify logic without hitting FCM API
2. **Test with Real FCM**: 
   - Configure valid FCM credentials
   - Submit an urgent contact form message
   - Verify push notification is received on your device

### Test Checklist

- [ ] Push notification sent for urgent messages
- [ ] No push notification for normal messages
- [ ] Push notification skipped when disabled in settings
- [ ] Error handling works when FCM credentials are invalid
- [ ] Notification tracking updated correctly in database
- [ ] Email notifications still work alongside push notifications

## Notification Payload

The push notification sent to FCM includes:

```json
{
  "to": "device_token",
  "priority": "high",
  "notification": {
    "title": "📩 Priority Message Received!",
    "body": "From: John Doe\nSubject: Urgent Project\nPlease respond within 24 hours.",
    "sound": "default",
    "badge": "1"
  },
  "data": {
    "contact_id": "123",
    "sender_name": "John Doe",
    "sender_email": "john@example.com",
    "subject": "Urgent Project",
    "message_snippet": "I need help with...",
    "submitted_date": "2025-10-12T23:58:00Z",
    "is_urgent": "true",
    "type": "priority_contact"
  }
}
```

## Email Template Enhancement

The admin notification email is automatically enhanced when a message is urgent:

- 🚨 **Subject Line**: Prefixed with "URGENT:"
- 🔴 **Visual Styling**: Red header and warning banner
- ⏰ **Response Reminder**: 24-hour response expectation highlighted

## Admin Interface

### ContactNotification Admin

New fields displayed:
- `push_notification_sent` - Boolean indicating if push was sent
- `is_urgent` - Shows if the contact message was marked urgent
- `push_notification_sent_at` - Timestamp of push notification

### NotificationSettings Admin

New section: **Push Notification Settings**
- `push_notification_enabled` - Enable/disable feature
- `fcm_server_key` - Firebase server key
- `fcm_device_token` - Device registration token

## Troubleshooting

### Push Notifications Not Sent

**Check 1: Settings Configuration**
```python
settings = NotificationSettings.get_settings()
print(f"Push enabled: {settings.push_notification_enabled}")
print(f"Server key: {settings.fcm_server_key[:10]}...")  # First 10 chars
print(f"Device token: {settings.fcm_device_token[:10]}...")
```

**Check 2: Message Urgency**
- Verify the contact submission has `is_urgent=True`
- Check ContactNotification record for error messages

**Check 3: FCM Credentials**
- Validate server key in Firebase Console
- Ensure device token is current (tokens can expire)

**Check 4: Logs**
```bash
tail -f logs/notifications.log
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `InvalidRegistration` | Device token is invalid/expired | Get a new device token from your app |
| `Unauthorized` | Server key is incorrect | Verify server key in Firebase Console |
| `Network timeout` | FCM endpoint unreachable | Check internet connectivity |
| `Missing credentials` | Settings not configured | Configure in Django Admin |

## Security Considerations

1. **Never commit credentials** - Keep FCM keys in `.env` file, not in code
2. **Use environment variables** - Settings can override from `FCM_SERVER_KEY` and `FCM_DEVICE_TOKEN`
3. **Validate device tokens** - Implement token refresh mechanism in your mobile app
4. **Rate limiting** - Consider adding rate limits to prevent notification spam
5. **Audit logs** - All notifications are tracked in `ContactNotification` model

## Future Enhancements

- [ ] Support for multiple device tokens (notify multiple devices)
- [ ] Web push notifications (using service workers)
- [ ] SMS fallback for critical notifications
- [ ] Custom notification sounds per priority level
- [ ] Analytics dashboard for notification delivery rates
- [ ] Scheduled retry for failed notifications
- [ ] Integration with other push services (OneSignal, Pushover)

## API Reference

### PushNotificationService

```python
from notifications.services import PushNotificationService

service = PushNotificationService()

# Send priority notification
success = service.send_priority_notification(
    contact_submission=contact,  # ContactSubmission instance
    notification=notification     # ContactNotification instance
)
```

### ContactNotification Methods

```python
# Mark push notification as sent
notification.mark_push_notification_sent()

# Mark push notification as failed
notification.mark_push_notification_sent(error="Error message")
```

## License

This feature is part of the portfolio project and follows the same license.

## Support

For issues or questions:
1. Check existing GitHub issues
2. Review logs: `logs/notifications.log`
3. Run test suite to verify setup
4. Create a new issue with error details

---

**Last Updated**: October 2025  
**Version**: 1.0.0
