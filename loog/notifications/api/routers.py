from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

api_router = DefaultRouter()
api_router.register('notifications', views.NotificationViewSet, 'notifications')

urlpatterns = [
    path('v1/', include(api_router.urls)),    
]
