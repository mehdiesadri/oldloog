from django.test import TestCase

from accounts.models import User

from discovery.utils import parse_query, generate_ngrams, update_inverted_index, find_users
from discovery.models import TagAssignment, Tag


class QueryTestCase(TestCase):
    def setUp(self) -> None:
        self.query = "django developer in germany"

    def test_valid_parse_query(self):
        tokens = parse_query(self.query)
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens, ['django', 'developer', 'germany'])

    def test_empty_parse_query(self):
        tokens = parse_query("")
        self.assertEqual(len(tokens), 0)
        self.assertEqual(tokens, [])

    def test_valid_generate_ngrams(self):
        two_grams = generate_ngrams(
            parse_query(self.query),
            n=2
        )
        self.assertIsInstance(two_grams, zip)
        self.assertEqual(
            list(two_grams),
            [
                ('django', 'developer'),
                ('developer', 'germany')
            ]
        )

    def test_invalid_generate_ngrams(self):
        self.assertRaises(
            AssertionError,
            lambda: generate_ngrams(
                parse_query(self.query),
                n=5
            )
        )


class InvertedIndexTestCase(TestCase):
    def setUp(self) -> None:
        self.tag = Tag.objects.create(name="django")
        self.test_user = User.objects.create(
            username="test_user0",
            email="test_user0@gmail.com",
            password="test12340"
        )
        self.giver = User.objects.create(
            username="test_user1",
            email="test_user1@gmail.com",
            password="test12341"
        )
        self.receiver = User.objects.create(
            username="test_user2",
            email="test_user2@gmail.com",
            password="test12342"
        )
        self.assignment = TagAssignment.objects.create(
            giver=self.giver,
            receiver=self.receiver,
            tag=self.tag
        )

    def test_update_inverted_index(self):
        inverted_index = update_inverted_index()
        self.assertIsInstance(inverted_index, dict)
        self.assertEqual(len(inverted_index), 1)
        tagged_user_id, tagged_count = inverted_index.get(self.tag.name)[0]
        self.assertEqual(tagged_user_id, self.receiver.id)
        self.assertEqual(tagged_count, 1)

    def test_valid_find_users(self):
        scores = find_users("django developer")
        self.assertEqual(len(scores), 1)
        self.assertEqual(list(scores.keys()), [self.receiver.id, ])
        self.assertEqual(scores.get(self.receiver.id, 0), 1)

    def test_invalid_find_users(self):
        scores = find_users("an invalid query")
        self.assertEqual(len(scores), 0)
