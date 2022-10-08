from django.contrib.admin import register, ModelAdmin
from chat.models import Message, ChatSession, ChatSessionUser


@register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ['session', 'sender', 'text', 'has_attachment']
    search_fields = ['session', 'sender', 'text']


@register(ChatSession)
class ChatSessionAdmin(ModelAdmin):
    list_display = ['room_name', 'is_expired']
    search_fields = ['room_name', 'query']


@register(ChatSessionUser)
class ChatSessionUserAdmin(ModelAdmin):
    list_display = ['session', 'user', 'is_tagged']
    list_filter = ['is_tagged']
    search_fields = ['session', 'user']
