from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<str:username>", views.get_profile),
    path("sit/<str:username>", views.set_initial_tags),
]
