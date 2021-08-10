from rest_framework import mixins, viewsets, permissions

from accounts.models import Profile, User
from .serializers import ProfileSerializer, UserSerializer


class UsersViewSet(mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permissions = (permissions.IsAdminUser,)


class ProfilesViewSet(mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAdminUser,)
