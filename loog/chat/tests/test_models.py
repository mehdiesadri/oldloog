from django.urls import reverse
from django.test import TestCase

from chat.models import ChatSession


class ChatSessionTestCase(TestCase):
    """
    Tests the login behind the ChatSession Model.
    """

    def setUp(self):
        self.session = ChatSession.objects.create(query="this is a test query", room_name="test_room")
    
    def test_string_representation(self):
        self.assertEqual("Room: test_room", str(self.session))

    def test_get_expire_datetime(self):
        dt = self.session.get_expire_datetime()
        delta = dt - self.session.created_at
        self.assertEqual(delta.seconds, 330)
    
    def test_get_absolute_url(self):
        expected = reverse("chat:join-session", kwargs={"room_name": "test_room"})
        self.assertEqual(expected, self.session.get_absolute_url())
