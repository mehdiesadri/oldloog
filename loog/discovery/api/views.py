import uuid

from rest_framework import mixins, viewsets, permissions, generics, status
from rest_framework.response import Response

from discovery.models import Tag, TagAssignment
from discovery.utils import find_users, send_notifications
from chat.models import ChatSession, ChatSessionUser
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
        user = self.request.user
        query = self.request.query_params.get('query', '').strip()
        
        if query == '':
            return Response(
                data={
                    "error": "Required query parameter: query."
                    },
                status=status.HTTP_400_BAD_REQUEST
                )
        
        session_obj = ChatSession.objects.create(
           query=query,
           room_name=uuid.uuid4().hex[:10].upper()
        )
        ChatSessionUser.objects.create(
            user=user,
            session=session_obj
        )
        user_score = find_users(query)
        if self.request.user.id in user_score:
            user_score.pop(self.request.user.id)
        payload = {
            'head': 'New chat request',
            'body': f'Query: {query}',
            'url': session_obj.get_absolute_url(),
            'icon': self.request.user.profile.get_avatar()
        }
        send_notifications(user_score.keys(), payload)
        return User.objects.filter(id__in=user_score.keys())

