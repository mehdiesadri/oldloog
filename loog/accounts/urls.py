from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginPage.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/<str:uidb64_invite_id>/<str:token>/", views.RegisterView.as_view(), name='register'),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="profile_update"),
    path("invite/", views.InvitePage.as_view(), name="invite"),
]
