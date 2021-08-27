from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from .serializers import MessageSerializer, UserModelSerializer
from chat.models import Message, ChatSession


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """

    page_size = settings.MESSAGES_TO_LOAD


class SessionMessageAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = MessageSerializer

    def get_chat_session(self):
        return get_object_or_404(ChatSession, **self.kwargs)

    def get_queryset(self):
        session = self.get_chat_session()
        return session.messages.all()
    
    def perform_create(self, serializer):
        return serializer.save(
            sender=self.request.user,
            session=self.get_chat_session()
        )



class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    allowed_methods = ("GET", "HEAD", "OPTIONS")
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)
