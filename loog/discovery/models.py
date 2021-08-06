import logging
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from main.tokens import registration_token

User = get_user_model()
logger = logging.getLogger(__name__)


def get_invitation_code() -> str:
    """
    Returns a unique six-character code
    """
    code = uuid4().hex[:10]
    logger.info(f"Generated a new invitation code: {code}")
    return str(code)


class Tag(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=32)
    value = models.IntegerField(verbose_name=_("Value"), default=-1)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name=_("User"))
    avatar = models.ImageField(verbose_name=_("Avatar"), upload_to='user_profiles/', blank=True, null=True)
    bio = models.TextField(verbose_name=_("Biography"), max_length=256, blank=True, null=True)
    location = models.CharField(verbose_name=_("Location"), max_length=64, blank=True, null=True)

    tags = models.ManyToManyField(to=Tag, verbose_name=_("Tags"), blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ("user",)

    @property
    def is_completed(self):
        """
        Indicates whether the profile is completed or not.
        """
        if self.avatar and self.bio and self.location:
            return True
        return False

    def get_invite_link(self):
        """
        Returns relative register path for the invitee.
        """
        base64_encoded_id = urlsafe_base64_encode(force_bytes(self.user_id))
        token = registration_token.make_token(self.user)
        register_url_args = {'uidb64': base64_encoded_id, 'token': token}
        register_path = reverse('main:register', kwargs=register_url_args)
        return register_path


class InvitedUsers(models.Model):
    inviter = models.ForeignKey(verbose_name=_("Inviter"), to=User, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name=_("Email"))
    is_registered = models.BooleanField(verbose_name=_("Registered"), default=False)
    initial_tags = models.ManyToManyField(to=Tag, verbose_name=_("Initial tags"))

    def __str__(self):
        return f"{self.email} invited by {self.inviter}"


class TagAssignment(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    giver = models.ForeignKey(
        Profile, on_delete=models.PROTECT, related_name="reciever"
    )
    reciever = models.ForeignKey(Profile, on_delete=models.PROTECT)
    time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=20)
