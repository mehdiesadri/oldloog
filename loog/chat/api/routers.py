from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MessageModelViewSet, UserModelViewSet


api_router = DefaultRouter()
api_router.register("message", MessageModelViewSet, basename="message-api")
api_router.register("user", UserModelViewSet, basename="user-api")

urlpatterns = [
    path('v1/', include(api_router.urls))
]
