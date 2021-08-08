from django.urls import path
from . import views

app_name = "discovery"

urlpatterns = [
    path("", views.index, name="discovery_index"),
    path("invite/", views.InvitePage.as_view(), name="invite"),
    path("profile/", views.get_profile, name="profile"),
    path("profile/set-tags/", views.InviteeTagPage.as_view(), name="profile_set_tag"),
    path("profile/update/", views.ProfileUpdatePage.as_view(), name="profile_update"),
    path("sit/<str:username>", views.set_initial_tags, name="tag"),
]
