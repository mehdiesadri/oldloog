from django.db import models
from django.urls import reverse

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

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

    # def characters(self):
    #     """
    #     Toy function to count body characters.
    #     :return: body's char number
    #     """
    #     return len(self.body)

    # def notify_ws_clients(self):
    #     """
    #     Inform client there is a new message.
    #     """
    #     notification = {
    #         "type": "receive_group_message",
    #         "message": "{}".format(self.id),
    #     }

    #     channel_layer = get_channel_layer()
    #     print("user.id {}".format(self.user.id))
    #     print("user.id {}".format(self.recipient.id))

    #     async_to_sync(channel_layer.group_send)("{}".format(self.user.id), notification)
    #     async_to_sync(channel_layer.group_send)(
    #         "{}".format(self.recipient.id), notification
    #     )

    # def save(self, *args, **kwargs):
    #     """
    #     Trims white spaces, saves the message and notifies the recipient via WS
    #     if the message is new.
    #     """
    #     new = self.id
    #     self.body = self.body.strip()  # Trimming whitespaces from the body
    #     super(MessageModel, self).save(*args, **kwargs)
    #     if new is None:
    #         self.notify_ws_clients()
