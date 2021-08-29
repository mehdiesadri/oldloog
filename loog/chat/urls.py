from django.urls import path

from . import views

app_name = "chat"


urlpatterns = [
    path("history/", views.ChatSessionList.as_view(), name="user-session-list"),
    path("<str:room_name>/", views.ChatSession.as_view(), name="session")
]
