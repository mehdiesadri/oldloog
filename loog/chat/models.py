from django.db import models
from django.urls import reverse

from accounts.models import User
from core.models import DateTimeModel


class ChatSession(DateTimeModel):
    query = models.CharField(verbose_name="query", max_length=1024)
    room_name = models.CharField(max_length=2048)

    def __str__(self) -> str:
        return f"Room: {self.room_name}"

class ChatSessionUser(DateTimeModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="user",
        related_name="user",
        db_index=True,
    )
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user} | {self.session}"
    
    def get_absolute_url(self):
        return reverse("chat:session", kwargs={"room_name": self.session.room_name})
    


class Message(DateTimeModel):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="user",
        related_name="from_user",
        db_index=True,
    )
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        verbose_name="session",
        related_name="messages",
        db_index=True,
    )
    text = models.CharField(max_length=512)
    attachment = models.FileField(upload_to="chats/", blank=True, null=True)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering = ("-created_at", )
