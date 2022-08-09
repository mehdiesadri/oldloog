import logging
import pickle
from collections import defaultdict
from datetime import datetime

import pytz
import redis
from django.conf import settings
from django.db.models import Count
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

from notifications.models import Notification
from .models import TagAssignment, Tag

logger = logging.getLogger(__name__)
redis_db = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=2
)


def get_tag_counts_in_assignments(assignments) -> dict:
    annotated_tags = assignments.values_list('tag__name').annotate(total=Count('tag')).order_by('-total')[:100]
    tag_counts = {}
    for tag_name, tag_count in annotated_tags:
        tag_counts[tag_name] = tag_count
    return tag_counts


def parse_query(query: str) -> list:
    """
    Gets a string and converts it to a list of tokens.

    Args:
        query: A string sentence.

    Returns:
        List of words with removing stopwords.
    """
    words = word_tokenize(query)
    stop_words = stopwords.words()
    tokens = [w for w in words if not w.lower() in stop_words]
    return tokens


def generate_ngrams(tokens, n=3):
    """
    gets tokens and converts it to 2-grams or 3-grams.

    Args:
        tokens: List of tokens.
        n: An integer number, 2 or 3

    Returns:
        List of ngrams.
    """
    assert (1 < n < 4), "n can only be 2 or 3"
    return ngrams(tokens, n)


def update_inverted_index():
    # key: tag, value: {(user, count),...}
    last_update = None  # redis_db.get("INVERTED_INDEX_UPDATED_DATETIME")
    if last_update is not None:
        last_update = last_update.decode('utf-8')
        last_update = datetime.strptime(last_update, "%m/%d/%Y, %H:%M:%S")
        last_update = last_update.replace(tzinfo=pytz.UTC)
    else:
        last_update = datetime(year=1900, month=1, day=1, tzinfo=pytz.UTC)

    all_tags = Tag.objects.all()
    for tag in all_tags:
        annotated_tags = TagAssignment.objects.filter(tag=tag, updated_at__gt=last_update).values_list(
            'receiver').annotate(
            total=Count('receiver')).order_by('-total')
        redis_db.set(str(tag.name), pickle.dumps(annotated_tags))


def find_users(query: str):
    user_score = defaultdict(int)
    one_grams = parse_query(query)
    two_grams = generate_ngrams(one_grams, n=2)
    three_grams = generate_ngrams(one_grams, n=3)
    grams = {
        3: three_grams,
        2: two_grams,
        1: one_grams,
    }
    for n, grams in grams.items():
        for gram in grams:
            gram = ' '.join(gram) if n > 1 else gram
            in_redis = redis_db.get(gram)
            if in_redis is None:
                logger.info(f"{gram} is not in redis.")
                continue
            user_counts = pickle.loads(in_redis)
            for i in user_counts:
                user_score[i[0]] += i[1] * n
    return user_score


def send_notifications(user_ids, payload):
    for user_id in user_ids:
        Notification.objects.create(
            user_id=user_id,
            is_internal=True,
            is_system=False,
            **payload
        )
