import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class RegistrationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.email)
        )


registration_token = RegistrationTokenGenerator()
