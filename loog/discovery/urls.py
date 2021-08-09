from django.urls import path
from . import views

app_name = "discovery"

urlpatterns = [
    path("", views.IndexPage.as_view(), name="discovery_index"),
    path("invite/", views.InvitePage.as_view(), name="invite"),
    path("profile/", views.ProfilePage.as_view(), name="profile"),
    path("profile/set-tags/", views.InviteeTagPage.as_view(), name="profile_set_tag"),
    path("profile/update/", views.ProfileUpdatePage.as_view(), name="profile_update"),
]
