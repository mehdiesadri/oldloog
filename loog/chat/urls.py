from django.urls import path

from . import views

app_name = "chat"


urlpatterns = [
    path("history/", views.ChatSessionList.as_view(), name="user-session-list"),
    path("<str:room_name>/", views.ChatSessionView.as_view(), name="session"),
    path("join/<str:room_name>/", views.join_chat_session, name="join-session")
]
