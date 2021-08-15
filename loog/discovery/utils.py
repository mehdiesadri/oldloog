from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

from collections import defaultdict

from django.db.models import Count

from .models import TagAssignment, Tag

INVERTED_INDEX = {}


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
    assert (1 < n < 4)
    return ngrams(tokens, n)


def update_inverted_index():
    # TODO: Celery every 5 minutes.
    # key: tag, value: {(user, count),...}
    global INVERTED_INDEX
    all_tags = Tag.objects.all()
    for tag in all_tags:
        annotated_tags = TagAssignment.objects.filter(tag=tag).values_list('receiver').annotate(
            total=Count('receiver')).order_by('-total')
        INVERTED_INDEX.update({tag.name: annotated_tags})
    return INVERTED_INDEX


def find_users(query: str):
    # TODO: Remove update after celery
    global INVERTED_INDEX
    update_inverted_index()

    user_score = defaultdict(int)
    one_grams = parse_query(query)
    two_grams = generate_ngrams(one_grams, n=2)
    three_grams = generate_ngrams(one_grams, n=3)
    print(one_grams, two_grams, three_grams, sep="\n")
    grams = {
        3: three_grams,
        2: two_grams,
        1: one_grams,
    }
    for n, grams in grams.items():
        for gram in grams:
            gram = ' '.join(gram) if n > 1 else gram
            user_counts = INVERTED_INDEX.get(gram)
            if user_counts:
                print(f"Fount {n}grams", gram, user_counts)
                for i in user_counts:
                    user_score[i[0]] += i[1] * n
    return user_score
