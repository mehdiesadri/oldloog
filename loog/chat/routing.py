from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]
