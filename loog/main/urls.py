from django.urls import path, re_path

from . import views

app_name = "main"


urlpatterns = [
    path("", views.HomePage.as_view(), name="homepage"),
    path("login/", views.LoginPage.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/<str:uidb64_invite_id>/<str:token>/", views.RegisterView.as_view(), name='register'),
    path("search/", views.search, name="search"),
]
