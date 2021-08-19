from django.test import TestCase
from django.urls import resolve

from accounts.models import User, InvitedUser
from accounts.selectors import get_invites_count, get_inviter, get_invite_obj_from_url


class InviteUserTestCase(TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create(
            username="test_user",
            email="test_user@gmail.com",
            password="test1234"
        )
        self.invited_user = InvitedUser.objects.create(
            inviter=self.test_user,
            email="test@test.com",
            is_registered=True,
            comma_separated_tags="tag1,tag2,tag3,tag4,tag4"
        )

    def test_invites_count(self):
        """
        Checks if function works correctly.
        """
        invites_count = get_invites_count(self.test_user)
        self.assertEqual(invites_count, 1)

    def test_valid_get_inviter(self):
        """
        Check if function returns correct inviter.
        """
        inviter = get_inviter("test@test.com")
        self.assertEqual(inviter, self.test_user)

    def test_invalid_get_inviter(self):
        """
        Checks if function raises correct exception.
        """
        self.assertRaises(InvitedUser.DoesNotExist, get_inviter, user_email="does-not-exists@gmail.com")

    def test_valid_get_invite_obj_from_url(self):
        link = self.invited_user.get_invite_link()
        resolved = resolve(link)
        uid = resolved.kwargs.get("uidb64_invite_id", "fake-uid")
        inviter = get_invite_obj_from_url(uid)
        self.assertEqual(inviter, self.invited_user)
        self.assertEqual(inviter.inviter, self.test_user)
