import logging

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import DateTimeModel

User = get_user_model()
logger = logging.getLogger(__name__)


class Tag(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=32)
    _type = models.IntegerField(verbose_name=_("Value"), default=-1)

    def __str__(self):
        return self.name


class TagAssignment(DateTimeModel):
    tag = models.ForeignKey(to=Tag, on_delete=models.PROTECT, verbose_name=_("Tag"))
    giver = models.ForeignKey(
        to=User, on_delete=models.PROTECT, related_name="receiver", verbose_name=_("Giver")
    )
    receiver = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name=_("Receiver"))

    def __str__(self):
        return f"{self.giver} --> {self.receiver}: {self.tag}"
