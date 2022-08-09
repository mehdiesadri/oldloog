import logging
from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from core.models import DateTimeModel
from core.tasks import send_email
from .tokens import registration_token

User = get_user_model()
logger = logging.getLogger(__name__)


class Profile(DateTimeModel):
    class UserPreferences(models.IntegerChoices):
        AS_MANY_AS_THERE = 1, _("Ask me as many as there")
        ALL_BUT_VERY_PICKY = 2, _("All but very picky")
        ONCE_A_DAY = 3, _("Once a day")
        MORNINGS_ONLY = 4, _("Mornings only")
        NOON_ONLY = 5, _("Around noon only")
        LATE_NIGHT_ONLY = 6, _("Late night only")
        WEEKENDS_ONLY = 7, _("Weekends only")
        ONCE_A_WEEK = 8, _("Once a week")

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name=_("User"))
    avatar = models.FileField(verbose_name=_("Avatar"), upload_to='user_profiles/', blank=True, null=True)
    location = models.CharField(verbose_name=_("Location"), max_length=64, blank=True, null=True)
    birthdate = models.DateField(verbose_name=_("Birthdate"), blank=True, null=True)
    preferences = models.IntegerField(verbose_name=_("User Preferences"), choices=UserPreferences.choices,
                                      default=UserPreferences.AS_MANY_AS_THERE)

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ("user",)

    @property
    def is_completed(self):
        """
        Indicates whether the profile is completed or not.
        """
        if self.avatar and self.birthdate and self.location:
            return True
        return False

    @property
    def age(self):
        if self.is_completed:
            today = date.today()
            return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url

    def get_name_or_username(self):
        return self.user.get_full_name() or self.user.username

    def get_preferences(self):
        return self.UserPreferences.choices[self.preferences][1]


class InvitedUser(DateTimeModel):
    inviter = models.ForeignKey(verbose_name=_("Inviter"), to=User, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name=_("Email"))
    is_registered = models.BooleanField(verbose_name=_("Registered"), default=False)
    comma_separated_tags = models.CharField(verbose_name=_("Comma Separated Tags"), max_length=1024)

    def send_invitation_email(self, host_name="127.0.0.1:8000"):
        return send_email(
            "Invitation Letter",
            f"You have been invited to Loog Project by {self.inviter}, "
            + f"You register link is: {host_name}{self.get_invite_link()}",
            [self.email]
        )

    def get_invite_link(self):
        """
        Returns relative register path for the invitee.
        """
        base64_encoded_id = urlsafe_base64_encode(force_bytes(self.id))
        token = registration_token.make_token(self.inviter)
        register_url_args = {'uidb64_invite_id': base64_encoded_id, 'token': token}
        register_path = reverse('accounts:register', kwargs=register_url_args)
        return register_path

    def __str__(self):
        return f"{self.email} invited by {self.inviter}"
