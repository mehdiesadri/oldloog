from django.urls import path

from notifications.consumers import NotificationConsumer
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/notifications/', NotificationConsumer.as_asgi()),
    path('ws/<str:room_name>/', ChatConsumer.as_asgi()),
]
