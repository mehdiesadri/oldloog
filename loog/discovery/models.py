from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Tag(models.Model):
    value = models.CharField(max_length=120)
    type = models.CharField(max_length=20)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class TagAssignment(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
    giver = models.ForeignKey(
        Profile, on_delete=models.PROTECT, related_name="reciever"
    )
    reciever = models.ForeignKey(Profile, on_delete=models.PROTECT)
    time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=20)
