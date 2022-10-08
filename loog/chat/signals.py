from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .api.serializers import MessageSerializer
from .models import Message


@receiver(post_save, sender=Message)
def chat_notification(sender, instance, created, **kwargs):
    """
    Sends the message to room via ChatConsumer.
    """

    if created:
        notification = {
            "type": "chat_message",
            "message": "chat",
            "data": MessageSerializer(instance=instance).data
        }
        # TODO: use Notification model instead!
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "chat_{}".format(instance.session.room_name), notification
        )
