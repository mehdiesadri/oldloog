from django.contrib.auth.decorators import login_required
from django.views import generic


from .models import ChatSessionUser


class ChatSessionList(generic.ListView):
    template_name = "chat/chat_list.html"
    
    def get_queryset(self):
        return ChatSessionUser.objects.filter(user=self.request.user)


class ChatSession(generic.TemplateView):
    template_name = "chat/chat.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_name"] = self.kwargs.get("room_name")
        return context
