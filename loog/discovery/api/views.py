from rest_framework import mixins, permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from discovery.models import Tag
from .serializers import TagSerializer


class TagViewSet(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 GenericViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
