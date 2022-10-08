from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import Notification


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, *args, **kwargs):
    """
    Sends alerts, emails, etc when a new notification is created.
    """
    if created:
        instance.send()
