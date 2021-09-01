from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

api_router = DefaultRouter()
api_router.register('tags', views.TagViewSet, 'tags')
api_router.register('assignments', views.TagAssignmentViewSet, 'assignments')
api_router.register('user-assignments', views.UserTagAssignmentViewSet, 'user-assignments')

urlpatterns = [
    path('v1/', include(api_router.urls)),
    path('v1/search-user/', views.SearchUserAPI.as_view(), name='search-user-api')
]
