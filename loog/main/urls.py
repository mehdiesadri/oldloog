from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.HomePage.as_view(), name="homepage"),
    path("about/", views.AboutPage.as_view(), name="about_page"),
]
