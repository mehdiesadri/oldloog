from rest_framework import mixins, viewsets, permissions

from notifications.models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NotificationSerializer
    pagination_class = None

    # def put(self, *args, **kwargs):
    #     return self.partial_update(*args, **kwargs)

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user,
            read=False,
            is_system=False,
            is_internal=True
        )
