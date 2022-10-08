from django.db import models


class DateTimeModel(models.Model):
    """
    Abstract date-time model.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
