from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.views import generic
from django.shortcuts import get_object_or_404
from nltk.util import pr


from .models import ChatSessionUser, ChatSession



class ChatSessionList(generic.ListView):
    template_name = "chat/chat_list.html"
    
    def get_queryset(self):
        return ChatSessionUser.objects.filter(user=self.request.user)


class ChatSessionView(generic.TemplateView):
    template_name = "chat/chat.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_name = self.kwargs.get("room_name")
        session_obj = get_object_or_404(ChatSession, room_name=room_name)
        context["room_name"] = room_name
        context["session_obj"] = session_obj
        return context

@login_required
def join_chat_session(request, room_name):
    print(room_name)
    return HttpResponse("OK")
