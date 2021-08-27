from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SessionMessageAPI, UserModelViewSet


api_router = DefaultRouter()
api_router.register("user", UserModelViewSet, basename="user-api")

urlpatterns = [
    path('v1/', include(api_router.urls)),
    path('v1/session/<str:room_name>/message/', SessionMessageAPI.as_view(), name='session-message-api')
]
