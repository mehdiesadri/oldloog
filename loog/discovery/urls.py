from django.urls import path
from . import views

app_name = "discovery"

urlpatterns = [
    path("", views.IndexPage.as_view(), name="discovery_index"),
    path("search/", views.search, name="search"),
]
