from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from nltk.util import pr

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from webpush import send_user_notification

from .utils import send_mail_to

logger = get_task_logger(__name__)

@shared_task
def send_email(*args, **kwargs):
    send_mail_to(*args, **kwargs)
    logger.info(f"An email sent to {kwargs.get('receivers', [])}")

@shared_task
def send_in_app_notification(user_id: int, payload: dict):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"chat_{user_id}", payload
        )

@shared_task
def send_web_push_notification(user_id: int, payload: dict, ttl: int = 1000):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    notification = {
            "type": "notification_message",
            "message": "New",
        }

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"chat_{user_id}", notification
        )
    
    send_user_notification(
        user=user,
        payload=payload,
        ttl=ttl
    )
    logger.info(f"A WPN send to {user}")
