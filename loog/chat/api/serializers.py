from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from chat.models import Message, ChatSessionUser
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    avatar = serializers.ReadOnlyField(source="sender.profile.get_avatar")
    user = serializers.ReadOnlyField(source="sender.username")
    
    class Meta:
        model = Message
        fields = ("id", "sender", "session", "text", "attachment", "created_at", "avatar", "user", )
        read_only_fields = ("id", "sender", "session", "created_at", "avatar", "user", )        


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSessionUser
        fields = ("id", "user", "session", "is_tagged", )
        read_only_fields = ("id", )
