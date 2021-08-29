from rest_framework import mixins, viewsets, permissions, generics, status
from rest_framework.response import Response

from discovery.models import Tag, TagAssignment
from discovery.utils import find_users, send_notifications

from accounts.api.serializers import UserSerializer
from accounts.models import User
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


class SearchUserAPI(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query')
        if query is None:
            return Response(
                data={
                    "error": "Required query parameter: query."
                    },
                status=status.HTTP_400_BAD_REQUEST
                )
        user_score = find_users(query)
        if self.request.user.id in user_score:
            user_score.pop(self.request.user.id)
        send_notifications(user_score.keys())
        return User.objects.filter(id__in=user_score.keys())

