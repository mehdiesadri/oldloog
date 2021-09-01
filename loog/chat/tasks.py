from celery import shared_task
from celery.utils.log import get_task_logger

from .models import ChatSession

logger = get_task_logger(__name__)

@shared_task
def make_chat_session_expire(chat_session_id):
    chat_session = ChatSession.objects.get(pk=chat_session_id)
    chat_session.is_expired = True
    chat_session.save()

    # TODO: Notify users

