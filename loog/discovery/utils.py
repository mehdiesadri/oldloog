from collections import defaultdict

from django.db.models import Count

from .models import TagAssignment, Tag

INVERTED_INDEX = {}


def get_tag_counts_in_assignments(assignments) -> dict:
    annotated_tags = assignments.values_list('tag__name').annotate(total=Count('tag')).order_by('-total')
    tag_counts = {}
    for tag_name, tag_count in annotated_tags:
        tag_counts[tag_name] = tag_count
    return tag_counts


def get_english_stop_words() -> list:
    """
    Returns english stop words.
    HINT: we can use NLTK library to support different languages.
    """
    return ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
            'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
            'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
            'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
            'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
            'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
            'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
            'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
            'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't",
            'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn',
            "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't",
            'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't",
            'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


def parse_query(query: str) -> list:
    """
    Gets a string and converts it to a list of tokens.

    Args:
        query: A string sentence.

    Returns:
        List of words with removing stopwords.
    """
    words = query.split()
    stop_words = get_english_stop_words()
    words = [w for w in words if not w.lower() in stop_words]
    return words


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
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]


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
    grams = {
        3: three_grams,
        2: two_grams,
        1: one_grams,
    }
    for n, grams in grams.items():
        for gram in grams:
            user_counts = INVERTED_INDEX.get(gram)
            if user_counts:
                print(f"Fount {n}grams", gram, user_counts)
                for i in user_counts:
                    user_score[i[0]] += i[1] * n
    return user_score
