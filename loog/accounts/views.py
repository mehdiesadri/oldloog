from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from core.mixins import ProfileRequiredMixin
from discovery.models import TagAssignment, Tag
from discovery.selectors import get_tag_count
from .forms import RegisterForm, ProfileForm
from .tokens import registration_token
from .utils import get_invite_obj_from_url


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
                return redirect("accounts:login")
        return HttpResponseForbidden(_("Sorry! You don't have access to this link..."))


class ProfileView(ProfileRequiredMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = "discovery/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfilePage, self).get_context_data(**kwargs)

        user = self.request.user
        profile = user.profile
        tags = {"gived": get_tag_count(giver=user), "recieved": get_tag_count(receiver=user)}
        context["tags"] = tags
        context["profile"] = profile
        return context


class ProfileUpdateView(SuccessMessageMixin, LoginRequiredMixin, generic.FormView):
    template_name = "discovery/profile_update.html"
    form_class = ProfileForm
    success_url = reverse_lazy("accounts:profile")
    success_message = _("You profile successfully updated.")

    def get_form(self, form_class=ProfileForm):
        profile = self.request.user.profile
        return form_class(instance=profile, **self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(ProfileUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user.is_staff:
            return context

        # inviter = get_inviter(self.request.user.email)
        # context["has_tag_form"] = not is_there_any_tag_assignment(giver=self.request.user, receiver=inviter)
        # context["inviter"] = inviter
        # context["tag_form"] = InviteeTagForm(initial={'user': inviter.id})

        return context

