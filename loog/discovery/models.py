from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    value = models.CharField(max_length=120)
    type = models.CharField(max_length=20)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class TagAssignment(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    giver = models.ForeignKey(
        Profile, on_delete=models.PROTECT, related_name="reciever"
    )
    reciever = models.ForeignKey(Profile, on_delete=models.PROTECT)
    time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=20)
