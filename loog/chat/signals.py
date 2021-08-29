from django.db.models.signals import post_save
from django.dispatch import receiver

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Message
from .api.serializers import MessageSerializer

# New message --> Notify users
@receiver(post_save, sender=Message)
def update_stock(sender, instance, created, **kwargs):
    if created:
        print(instance)
        notification = {
            "type": "chat_message",
            "message": MessageSerializer(instance=instance).data,
        }

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "chat_{}".format(instance.session.room_name), notification
            )
