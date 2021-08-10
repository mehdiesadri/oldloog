from rest_framework import serializers

from accounts.models import Profile, User, InvitedUser


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


class InvitedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitedUser
        fields = ["id", "inviter", "email", "is_registered", "comma_separated_tags", ]
        read_only_fields = ["id", ]
