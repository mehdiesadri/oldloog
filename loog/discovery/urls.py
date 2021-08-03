from django.urls import path
from . import views

app_name = "discovery"

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.get_profile, name="profile"),
    path("sit/<str:username>", views.set_initial_tags, name="tag"),
]
