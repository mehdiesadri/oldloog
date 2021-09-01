from django.db import models
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from core.models import DateTimeModel


class ChatSession(DateTimeModel):
    query = models.CharField(verbose_name="query", max_length=1024)
    room_name = models.CharField(max_length=12, unique=True)

    def __str__(self) -> str:
        return f"Room: {self.room_name}"
    
    @property
    def is_open_for_first_join(self):
        return (timezone.now() - self.created_at).seconds > 30

    @property
    def is_expired(self):
        return self.get_expire_datetime() < timezone.now()
    
    def get_expire_datetime(self):
        return self.created_at + timezone.timedelta(seconds=210)
    
    def get_absolute_url(self):
        return reverse("chat:join-session", kwargs={"room_name": self.room_name})
    

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
    
    class Meta:
        ordering = ("-created_at", )
    


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
