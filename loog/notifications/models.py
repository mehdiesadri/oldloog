from django.db import models

from accounts.models import User
from core.models import DateTimeModel
from core.tasks import send_email, send_in_app_notification


from firebase_admin.messaging import Notification as FirebaseNotification, Message
from fcm_django.models import FCMDevice


class Notification(DateTimeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    title = models.CharField(max_length=256)
    body = models.CharField(max_length=2048)
    icon_url = models.CharField(max_length=512, blank=True, null=True)
    url = models.CharField(max_length=512, blank=True, null=True)

    is_system = models.BooleanField(default=False)
    is_email = models.BooleanField(default=False)
    is_internal = models.BooleanField(default=False)
    is_webpush = models.BooleanField(default=False)

    def get_payload(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'body': self.body,
            'icon_url': self.icon_url,
            'url': self.url,
            'created_at': str(self.created_at)
        }

    def send_as_email(self):
        send_email.delay(
            subject=self.title,
            message=self.body,
            receivers=[self.user.email, ]
        )

    def send_as_internal(self):
        payload = self.get_payload()
        if self.is_system:
            payload.update({'type': 'system_message'})
        else:
            payload.update({'type': 'notification_message'})

        send_in_app_notification.delay(
            user_id=self.user.id,
            payload=payload
        )
    
    def send_as_webpush(self):
        payload = self.get_payload()

        if self.is_system:
            payload.update({'type': 'system_message'})
        else:
            payload.update({'type': 'notification_message'})

        try:
            notif = Message(
                data=payload,
            )
            device = FCMDevice.objects.get(user_id=self.user.id)
            device.send_message(notif)
            print("FCM message sent!")
        except FCMDevice.DoesNotExist as e:
            print("User has not device!", e)


    def __str__(self) -> str:
        return str(self.title)
