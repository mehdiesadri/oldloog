from celery.utils.log import get_task_logger
from celery.schedules import crontab

from loog.celery import app
from .utils import update_inverted_index

logger = get_task_logger(__name__)

@app.task
def updating_inverted_index():
    logger.info("Updating inverted index...")
    update_inverted_index()

app.add_periodic_task(
    10.0, 
    updating_inverted_index,
    name="updating_inverted_index"
)
