from celery import shared_task
from celery.utils.log import get_task_logger

from webpush import send_user_notification

from .utils import send_mail_to

logger = get_task_logger(__name__)

@shared_task
def send_email(*args, **kwargs):
    send_mail_to(*args, **kwargs)
    logger.info(f"An email sent to {kwargs.get('receivers', [])}")

@shared_task
def send_web_push_notification(user, payload: dict, ttl: int = 1000):
    send_user_notification(
        user=user,
        payload=payload,
        ttl=ttl
    )
    logger.info(f"A WPN send to {user}")
