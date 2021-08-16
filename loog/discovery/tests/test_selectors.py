from django.test import TestCase

from accounts.models import User

from discovery.models import TagAssignment, Tag
from discovery.selectors import get_tag_by_name, is_there_any_tag_assignment, get_tag_count


class TagTestCase(TestCase):
    def setUp(self) -> None:
        self.tag = Tag.objects.create(name="django")

    def test_get_tag_by_name(self):
        tag = get_tag_by_name("django")
        self.assertEqual(tag, self.tag)
        get_tag_by_name("python")
        self.assertEqual(Tag.objects.all().count(), 2)


class TagAssignmentTestCase(TestCase):
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

    def test_valid_is_there_any_tag_assignment(self):
        is_there = is_there_any_tag_assignment(giver=self.giver, receiver=self.receiver)
        self.assertTrue(is_there)

    def test_invalid_is_there_any_tag_assignment(self):
        is_there = is_there_any_tag_assignment(giver=self.giver, receiver=self.giver)
        self.assertFalse(is_there)

    def test_get_tag_count(self):
        tag_count = get_tag_count(giver=self.giver)
        self.assertEqual(tag_count, {self.tag.name: 1})

        tag_count = get_tag_count(giver=self.test_user)
        self.assertEqual(tag_count, {})
