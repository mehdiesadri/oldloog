import operator

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login")
def start_chat(request, matchingProfiles=None):
    print("############")
    print(matchingProfiles)
    return render(
        request=request,
        template_name="chat/chat.html",
    )
