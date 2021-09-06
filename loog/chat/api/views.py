from django.shortcuts import get_object_or_404
from rest_framework import views, generics, viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import ChatSession, ChatSessionUser
from .serializers import MessageSerializer, UserSessionSerializer


class SessionMessageAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_chat_session(self):
        return get_object_or_404(ChatSession, **self.kwargs)

    def get_queryset(self):
        session = self.get_chat_session()
        return session.messages.all()

    def perform_create(self, serializer):
        if self.get_chat_session().is_expired:
            raise ValidationError("Chat session is expired!")
        return serializer.save(
            sender=self.request.user,
            session=self.get_chat_session()
        )


class SessionExpireAPI(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get_session(self, room_name):
        return get_object_or_404(ChatSession, room_name=room_name)

    def get(self, request, room_name, *args, **kwargs):
        session = self.get_session(room_name)
        return Response({
            "timestamp": session.get_expire_datetime(),
            "is_expired": session.is_expired
        }, status=200)


class UserSessionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSessionSerializer

    def get_queryset(self):
        return ChatSessionUser.objects.filter(user=self.request.user)
