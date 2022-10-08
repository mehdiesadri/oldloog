from asgiref.sync import async_to_sync
from celery import shared_task
from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer

from django.conf import settings

from .utils import send_mail_to

logger = get_task_logger(__name__)


@shared_task
def _send_email(*args, **kwargs):
    send_mail_to(*args, **kwargs)
    logger.info(f"An email sent to {kwargs.get('receivers', [])}")


@shared_task
def _send_in_app_notification(user_id: int, payload: dict):
    channel_layer = get_channel_layer()
    # TODO: Dedicate a specific channel for notifications!
    async_to_sync(channel_layer.group_send)(
        f"chat_{user_id}", payload
    )

send_email = _send_email
send_in_app_notification = _send_in_app_notification

if settings.CELERY_ENABLED:
    send_email = _send_email.delay
    send_in_app_notification = _send_in_app_notification.delay
