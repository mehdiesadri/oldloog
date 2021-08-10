from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProfilesViewSet, UsersViewSet

api_router = DefaultRouter()
api_router.register('users', UsersViewSet, 'users')
api_router.register('profiles', ProfilesViewSet, 'profiles')

urlpatterns = [
    path('v1/', include(api_router.urls))
]
