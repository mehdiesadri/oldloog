from celery import shared_task
from celery.utils.log import get_task_logger

from .utils import send_mail_to

logger = get_task_logger(__name__)

@shared_task
def send_email(*args, **kwargs):
    logger.info("Sending email...")
    send_mail_to(*args, **kwargs)
