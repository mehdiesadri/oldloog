from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from chat.models import Message
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "sender", "session", "text", "attachment", )
        readonly_fields = ("id", "sender", "session", )


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)
