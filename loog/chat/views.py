from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="/login")
def start_chat(request):
    return render(
        request=request,
        template_name="chat/chat.html",
    )
