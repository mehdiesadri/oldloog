from django.contrib import messages
from django.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from core.tasks import send_in_app_notification
from core.mixins import ProfileRequiredMixin
from core.decorators import profile_required
from discovery.selectors import get_tag_count
from .models import ChatSessionUser, ChatSession
from .utils import is_session_invalid


class ChatSessionList(ProfileRequiredMixin, generic.ListView):
    template_name = "chat/chat_list.html"

    def get_queryset(self):
        return ChatSessionUser.objects.filter(user=self.request.user)


class ChatSessionView(ProfileRequiredMixin, generic.TemplateView):
    template_name = "chat/chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_name = self.kwargs.get("room_name")
        session_obj = get_object_or_404(ChatSession, room_name=room_name)
        context["session_obj"] = session_obj
        return context


@profile_required
def join_chat_session(request, room_name):
    session = get_object_or_404(ChatSession, room_name=room_name)
    if is_session_invalid(session):
        messages.error(request, _("Sorry, the requested room is not valid."))
        return redirect("main:homepage")

    in_session = session.chatsessionuser_set.all()
    in_session_count = in_session.count()
    in_session_first = in_session.first()

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


@profile_required
def session_post_tag(request, room_name):
    session = get_object_or_404(ChatSession, room_name=room_name)
    session_users = session.chatsessionuser_set.exclude(user=request.user)
    objects = []
    for i in session_users:
        objects.append({
            'id': i.id,
            'user': i.user,
            'top_tags': ','.join(list(get_tag_count(receiver=i.user).keys())[:2])
        })
    context = {
        'session': session,
        'objects': objects,
    }
    return render(request, "chat/post_tag.html", context)
