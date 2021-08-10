from rest_framework import viewsets, permissions

from accounts.models import Profile, User, InvitedUser
from .serializers import ProfileSerializer, UserSerializer, InvitedUserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permissions = (permissions.IsAdminUser,)


class ProfilesViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAdminUser,)


class InvitedUsersViewSet(viewsets.ModelViewSet):
    serializer_class = InvitedUserSerializer
    queryset = InvitedUser.objects.all()
    permissions = (permissions.IsAdminUser,)
