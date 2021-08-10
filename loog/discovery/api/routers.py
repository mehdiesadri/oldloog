from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, TagAssignmentViewSet

api_router = DefaultRouter()
api_router.register('tags', TagViewSet, 'tags')
api_router.register('assignments', TagAssignmentViewSet, 'assignments')

urlpatterns = [
    path('v1/', include(api_router.urls))
]
