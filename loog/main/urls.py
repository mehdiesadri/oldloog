from django.urls import path
from . import views

app_name = "main"


urlpatterns = [
    path("", views.HomePage.as_view(), name="homepage"),
    path("register/", views.RegisterPage.as_view(), name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("search/", views.search, name="search"),
]
