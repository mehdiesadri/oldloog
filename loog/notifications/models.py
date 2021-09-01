from django.db import models

from accounts.models import User
from core.models import DateTimeModel


class Notification(DateTimeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    title = models.CharField(max_length=256)
    body = models.CharField(max_length=2048)
    icon_url = models.CharField(max_length=512, blank=True, null=True)
    url = models.CharField(max_length=512, blank=True, null=True)

    is_email = models.BooleanField(default=False)
    is_webpush = models.BooleanField(default=False)
    is_internal = models.BooleanField(default=False)

    def get_payload(self):
        return {
                'head': self.title,
                'body': self.body,
                'icon': self.icon_url,
                'url': self.url
            }
    
    def __str__(self) -> str:
        return str(self.title)
