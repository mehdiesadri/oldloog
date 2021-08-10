from rest_framework import serializers

from accounts.models import Profile, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "avatar", "location", "birthdate", "preferences"]
        read_only_fields = ["id", "user", ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "profile", "username", "email", "first_name", "last_name", ]
        read_only_fields = ["id", "profile", "username", "email", ]
