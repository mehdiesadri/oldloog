from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginPage.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/<str:uidb64_invite_id>/<str:token>/", views.RegisterView.as_view(), name='register'),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/set-inviter-tags/", views.SetInviterTagView.as_view(), name="set_tags"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="profile_update"),
    path("invite/", views.InvitePage.as_view(), name="invite"),
    path("google/login/", views.google_login, name="google_login"),
    path("google/register/", views.google_register, name="google_register"),
    path("google/auth/", views.google_authorize, name="google_authorize"),
]
