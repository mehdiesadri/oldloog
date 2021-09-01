from django.db.models.signals import post_save
from django.dispatch import receiver

from core.tasks import send_email, send_web_push_notification, send_in_app_notification
from .models import Notification


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, *args, **kwargs):
    """
    Sends alerts, emails, etc when a new notification is created.
    """
    if created:
        if instance.is_email:
            send_email.delay(
                subject=instance.title,
                message=instance.body,
                receivers=[instance.user.email,]
            )
        if instance.is_webpush:
            send_web_push_notification.delay(
                user_id=instance.user.id,
                payload=instance.get_payload(),
                ttl=1500
            )
        if instance.is_internal:
            send_in_app_notification.delay(
                user_id=instance.user.id,
                payload=instance.get_payload()
            )
