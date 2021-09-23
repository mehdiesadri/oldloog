from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 'read', 'title', 'body',
            'icon_url', 'url', 'created_at',
            'is_system', 'is_email', 'is_internal',
            )
        read_only_fields = (
            'id', 'created_at',
        )
