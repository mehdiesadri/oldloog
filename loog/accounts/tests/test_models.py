from django.core import mail
from django.test import TestCase
from django.urls import resolve

from accounts.models import User, Profile, InvitedUser


# Best Practice: Signals are bad!


class CreateUserTestCase(TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create(
            username="test_user",
            email="test_user@gmail.com",
            password="test1234"
        )

    def test_post_save_signal(self):
        """
        Each user must have 1 profile.
        """
        profiles = Profile.objects.all()

        self.assertEqual(profiles.count(), 1)
        self.assertEqual(profiles.first().user, self.test_user)

    def test_profile_update(self):
        """
        Updating profile must not create new object.
        """
        self.test_user.profile.location = "Iran"
        self.test_user.profile.save()

        profiles = Profile.objects.all()

        self.assertEqual(profiles.count(), 1)
        self.assertEqual(profiles.first().location, "Iran")

    def test_profile_not_completed(self):
        """
        New profiles are in-complete.
        """
        self.assertFalse(self.test_user.profile.is_completed)


class InvitedUserTestCase(TestCase):
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
        mail.outbox = []

    def test_send_email(self):
        res = self.invited_user.send_invitation_email()
        self.assertEqual(res, 1)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn("You have been invited to Loog Project by", email.body)
        self.assertEqual(email.subject, "Invitation Letter")
        self.assertEqual(email.to, [self.invited_user.email, ])

    def test_invite_link(self):
        link = self.invited_user.get_invite_link()
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            resolve(link).view_name, 'accounts:register'
        )
