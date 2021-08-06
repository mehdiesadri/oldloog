from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "main"


urlpatterns = [
    path("", views.HomePage.as_view(), name="homepage"),
    path("register/", views.RegisterPage.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("search/", views.search, name="search"),
]
