import factory

from . import models


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Profile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    profile = factory.SubFactory(ProfileFactory)
