from django.contrib.admin import register, ModelAdmin
from chat.models import Message, ChatSession, ChatSessionUser


@register(Message)
class MessageAdmin(ModelAdmin):
    pass

@register(ChatSession)
class ChatSessionAdmin(ModelAdmin):
    pass


@register(ChatSessionUser)
class ChatSessionUserAdmin(ModelAdmin):
    pass
