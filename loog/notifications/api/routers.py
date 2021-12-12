from django.urls import path, include
from rest_framework.routers import DefaultRouter

from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from . import views

api_router = DefaultRouter()
api_router.register('notifications', views.NotificationViewSet, 'notifications')
api_router.register('devices', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    path('v1/', include(api_router.urls)),    
]
