from rest_framework import serializers

from discovery.models import Tag, TagAssignment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name", "_type", ]
        read_only_fields = ["_type", ]

    def create(self, validated_data):
        instance, _ = Tag.objects.get_or_create(**validated_data)
        return instance


class TagAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagAssignment
        fields = ["tag", "giver", "receiver", ]
