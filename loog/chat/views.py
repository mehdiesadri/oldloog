from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from core.tasks import send_in_app_notification
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
    session = get_object_or_404(ChatSession, room_name=room_name)
    in_session = session.chatsessionuser_set.all()
    in_session_count = in_session.count()
    in_session_first = in_session.first()
    user = request.user
    
    if in_session_count == 0 or session.is_expired or (in_session_count == 1 and session.is_open_for_first_join):        
        messages.error(request, "Cannot join to room")
        return redirect("main:homepage")
    
    if in_session_count == 1 and in_session_first == user:
        return redirect(in_session_first.get_absolute_url())
    
    
    session_user, _ = ChatSessionUser.objects.get_or_create(
        user=request.user,
        session=session
    )

    if in_session_count == 1:
        # Notify inviter
        payload = {
                "type": "notification_message",
                "message": "redirect",
                "data": {
                    "url":  session.get_absolute_url(),
                }
            }
        send_in_app_notification.delay(
            in_session_first.user.id,
            payload
            )
        
        
    return redirect(session_user.get_absolute_url())


@login_required
def session_post_tag(request, room_name):
    session = get_object_or_404(ChatSession, room_name=room_name)
    session_users = session.chatsessionuser_set.exclude(user=request.user).values('user')
    print(session_users)
    context = {
        'session': session
    }
    return render(request, "chat/post_tag.html", context)
