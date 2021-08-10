from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagViewSet

api_router = DefaultRouter()
api_router.register('tag', TagViewSet, 'tag')

urlpatterns = [
    path('v1/', include(api_router.urls))
]
