from django.test import TestCase

from accounts.models import User, Profile

# Best Practice: Signals are bad!


class CreateUserTestCase(TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create(
            username="test_user",
            email="test_user@gmail.com",
            password="test1234"
        )
        return super().setUp()
    
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

