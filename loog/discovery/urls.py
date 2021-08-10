from django.urls import path
from . import views

app_name = "discovery"

urlpatterns = [
    path("", views.IndexPage.as_view(), name="discovery_index"),
    path("invite/", views.InvitePage.as_view(), name="invite"),
    path("profile/set-tags/", views.InviteeTagPage.as_view(), name="profile_set_tag"),
]
