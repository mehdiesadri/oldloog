from django.urls import path
from . import views

app_name = "discovery"

urlpatterns = [
    path("", views.index, name="discovery_index"),
    path("invite/", views.InvitePage.as_view(), name="invite"),
    path("profile/", views.get_profile, name="profile"),
    path("profile/complete/", views.ProfileCompletePage.as_view(), name="profile_complete"),
    path("sit/<str:username>", views.set_initial_tags, name="tag"),
]
