from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat.api import MessageModelViewSet, UserModelViewSet
from . import views

app_name = "chat"

router = DefaultRouter()
router.register(r"message", MessageModelViewSet, basename="message-api")
router.register(r"user", UserModelViewSet, basename="user-api")

urlpatterns = [
    path(r"api/v1/", include(router.urls)),
    path("", views.start_chat, name="chat"),
]
