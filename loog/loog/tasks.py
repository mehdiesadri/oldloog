from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task
def debug_task():
    logger.info("Celery debug task executed. This runs every minute!")
