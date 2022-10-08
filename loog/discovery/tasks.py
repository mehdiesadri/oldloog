from django.utils import timezone

from celery.utils.log import get_task_logger

from loog.celery import app
from .utils import update_inverted_index, redis_db

logger = get_task_logger(__name__)

@app.task
def updating_inverted_index():
    logger.info("Updating inverted index...")
    update_inverted_index()
    redis_db.set('INVERTED_INDEX_UPDATED_DATETIME', timezone.now().strftime("%m/%d/%Y, %H:%M:%S"))

app.add_periodic_task(
    300.0,
    updating_inverted_index,
    name="updating_inverted_index"
)
