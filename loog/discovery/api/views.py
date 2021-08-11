from rest_framework import mixins, viewsets, permissions

from discovery.models import Tag, TagAssignment
from .serializers import TagSerializer, TagAssignmentSerializer


class TagViewSet(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """CR API of Tag for authenticated users"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagAssignmentViewSet(viewsets.ModelViewSet):
    """CRUD API of TagAssignment for admin users"""
    serializer_class = TagAssignmentSerializer
    permission_classes = (permissions.IsAdminUser, )
    queryset = TagAssignment.objects.all()
