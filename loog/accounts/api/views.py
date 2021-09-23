from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile, User, InvitedUser
from .serializers import ProfileSerializer, UserSerializer, InvitedUserSerializer, WaitListSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """CRUD API of User for admin users"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permissions = (permissions.IsAdminUser,)


class ProfilesViewSet(viewsets.ModelViewSet):
    """CRUD API of Profile for admin users"""
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAdminUser,)


class InvitedUsersViewSet(viewsets.ModelViewSet):
    """CRUD API of InvitedUser for admin users"""
    serializer_class = InvitedUserSerializer
    queryset = InvitedUser.objects.all()
    permissions = (permissions.IsAdminUser,)


class WaitListAPI(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        serializer = WaitListSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        admin_user = User.objects.filter(is_superuser=True).first()
        email = serializer.data.get('email')
        already_invited = InvitedUser.objects.filter(email=email).exists()
        if already_invited:
            return Response(data={"error": "Already invited!"}, status=400)

        obj = InvitedUser.objects.create(
            inviter=admin_user,
            email=email,
            comma_separated_tags='new user, wait list,'
        )
        obj.send_invitation_email(
            host_name=request.build_absolute_uri("/")[:-1]
        )
        return Response(data=serializer.data)
