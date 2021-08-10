from rest_framework import serializers

from discovery.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name", "_type", ]
        read_only_fields = ["_type", ]
