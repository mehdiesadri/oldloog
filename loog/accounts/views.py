from django.contrib import messages
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
from discovery.models import TagAssignment
from discovery.selectors import get_tag_count, get_tag_by_name
from .forms import RegisterForm, ProfileForm, InviteForm
from .selectors import get_invites_count
from .tokens import registration_token
from .utils import get_invite_obj_from_url


class LoginPage(auth_views.LoginView):
    """
    Session-based login.
    Note: It will redirect to homepage after a successful login.
    You can change this in settings --> LOGIN_REDIRECT_URL
    """
    # TODO: Add Social Auth
    template_name = "accounts/login.html"


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
            return render(request, 'accounts/register.html', context={'form': form, 'inviter': invite_obj.inviter})
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
                            tag=get_tag_by_name(tag),
                            receiver=new_user,
                            giver=invite_obj.inviter
                        )

                    for tag in form.cleaned_data.get("comma_separated_tags").split(","):
                        TagAssignment.objects.create(
                            tag=get_tag_by_name(tag),
                            receiver=invite_obj.inviter,
                            giver=new_user
                        )
                return redirect("accounts:login")
        return HttpResponseForbidden(_("Sorry! You don't have access to this link..."))


class ProfileView(ProfileRequiredMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        user = self.request.user
        profile = user.profile
        tags = {"gived": get_tag_count(giver=user), "recieved": get_tag_count(receiver=user)}
        context["tags"] = tags
        context["profile"] = profile
        return context


class ProfileUpdateView(SuccessMessageMixin, LoginRequiredMixin, generic.FormView):
    template_name = "accounts/profile_update.html"
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


class InvitePage(SuccessMessageMixin, ProfileRequiredMixin, LoginRequiredMixin, generic.CreateView):
    template_name = 'accounts/invite.html'
    form_class = InviteForm
    success_url = reverse_lazy("accounts:invite")
    success_message = _("You friend successfully invited. We will send him/her an invitation email.")

    def form_valid(self, form):
        invited = form.save(commit=False)
        if get_invites_count(self.request.user) <= 4:
            invited.inviter = self.request.user
            invited.save()
        else:
            messages.error(self.request, message=_("You cannot invite more than 5 friends."))
            return redirect("accounts:invite")
        return super(InvitePage, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(InvitePage, self).get_context_data(**kwargs)
        context['current_invites'] = get_invites_count(self.request.user)
        return context
