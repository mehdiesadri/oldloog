from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, TagAssignmentViewSet

api_router = DefaultRouter()
api_router.register('tag', TagViewSet, 'tag')
api_router.register('tag_assignment', TagAssignmentViewSet, 'tag_assignment')

urlpatterns = [
    path('v1/', include(api_router.urls))
]
