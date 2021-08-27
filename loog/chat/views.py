from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from .models import ChatSessionUser


@login_required(login_url="/login")
def start_chat(request):
    user_sessions = ChatSessionUser.objects.filter(user=request.user)
    return render(
        request=request,
        template_name="chat/chat.html",
        context={
            "user_sessions": user_sessions
        }
    )
