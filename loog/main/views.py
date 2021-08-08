from django.contrib.auth import views as auth_views
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import generic

from discovery.models import TagAssignment, Tag
from discovery.views import discover
from .tokens import registration_token
from .forms import RegisterForm
from .utils import get_invite_obj_from_url


class HomePage(generic.TemplateView):
    """
    Simple template view for rendering the home page of website.
    """
    template_name = "main/main.html"


class LoginPage(auth_views.LoginView):
    """
    Session-based login.
    Note: It will redirect to homepage after a successful login.
    You can change this in settings --> LOGIN_REDIRECT_URL
    """
    # TODO: Add Social Auth
    template_name = "main/login.html"


class LogoutView(auth_views.LogoutView):
    """
    Session-based logout.
    Note: It will redirect to login page after a successful logout.
    You can change this in settings --> LOGOUT_REDIRECT_URL
    """
    pass


class RegisterView(generic.View):
    # TODO: Add social auth
    def get(self, request, uidb64_invite_id, token):
        invite_obj = get_invite_obj_from_url(uidb64_invite_id)
        if invite_obj is not None and registration_token.check_token(invite_obj.inviter, token):
            form = RegisterForm(
                initial={'email': invite_obj.email},
            )
            return render(request, 'main/register.html', context={'form': form})
        else:
            return HttpResponseForbidden("Sorry! You don't have access to this link...")

    def post(self, request, uidb64_invite_id, token):
        invite_obj = get_invite_obj_from_url(uidb64_invite_id)
        if invite_obj is not None and registration_token.check_token(invite_obj.inviter, token):
            form = RegisterForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    new_user = form.save(commit=True)
                    invite_obj.is_registered = True
                    invite_obj.save()

                    for tag in invite_obj.comma_separated_tags.split(","):
                        TagAssignment.objects.create(
                            tag=Tag.objects.get_or_create(name=tag)[0],
                            receiver=new_user,
                            giver=invite_obj.inviter
                        )
                return redirect("main:login")
        return HttpResponseForbidden(_("Sorry! You don't have access to this link..."))


def search(request):
    if request.method == "POST":
        username = request.user.username
        query = request.POST.get("query")

    return discover(request, username, query)
