from django.db import models

from accounts.models import User
from core.models import DateTimeModel
from core.tasks import send_email, send_in_app_notification


class Notification(DateTimeModel):
    """
    For saving and handling user/system notifications!
    """
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
        payload = {
            'id': str(self.id),
            'title': self.title,
            'body': self.body,
            'icon_url': self.icon_url,
            'url': self.url,
            'created_at': str(self.created_at)
        }
        if self.is_system:
            payload.update({'type': 'system_message'})
        else:
            payload.update({'type': 'notification_message'})
        return payload

    def send_as_email(self):
        send_email(
            subject=self.title,
            message=self.body,
            receivers=[self.user.email, ]
        )

    def send_as_internal(self):
        payload = self.get_payload()

        send_in_app_notification(
            user_id=self.user.id,
            payload=payload
        )

    def send_as_webpush(self):
        # TODO: Implement webpush notification!
        raise NotImplementedError("The webpush notification is not supported yet!")

    def send(self):
        if self.is_email:
            self.send_as_email()
        if self.is_internal:
            self.send_as_internal()
        if self.is_webpush:
            self.send_as_webpush()

    def __str__(self) -> str:
        return str(self.title)
