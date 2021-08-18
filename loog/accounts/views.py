from authlib.integrations.django_client import OAuth

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
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
from discovery.selectors import get_tag_count, get_tag_by_name, is_there_any_tag_assignment
from discovery.forms import TagForm

from .forms import RegisterForm, ProfileForm, InviteForm
from .selectors import get_invites_count, get_inviter
from .tokens import registration_token
from .utils import get_invite_obj_from_url
from .models import User

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


def google_login(request):
    # build a full authorize callback uri
    redirect_uri = request.build_absolute_uri(
        reverse_lazy('accounts:google_authorize')
    )
    request.session['auth_method'] = 'login'
    return oauth.google.authorize_redirect(request, redirect_uri)


def google_register(request):
    redirect_uri = request.build_absolute_uri(
        reverse_lazy('accounts:google_authorize')
    )
    request.session['auth_method'] = 'register'
    request.session['invited_email'] = request.GET.get('email', '')
    request.session['inviter'] = request.GET.get('inviter', '')
    return oauth.google.authorize_redirect(request, redirect_uri)


def google_authorize(request):
    token = oauth.google.authorize_access_token(request)
    userinfo = oauth.google.parse_id_token(request, token)
    auth_method = request.session.pop('auth_method')
    print(auth_method)
    # Do login here
    email = userinfo.get("email")
    if email is None:
        messages.add_message(request, messages.ERROR, _("Google auth failed."))
        return redirect('accounts:login')

    users = User.objects.filter(email=email)
    users_count = users.count()

    if auth_method == 'login':
        if users_count == 1:
            login(request, users[0])
        elif users_count == 0:
            messages.error(request, _("You don't have account in Loog!"))
            return redirect('accounts:login')
        else:
            messages.error(request, _("Server Error 500, Call site admins!"))
            return redirect('accounts:login')
    elif auth_method == 'register':
        if users_count > 0:
            messages.error(request, _("Account already exists, try to login with google!"))
            return redirect('accounts:login')
        else:
            invited_email = request.session.pop('invited_email')
            inviter = request.session.pop('inviter')
            print(inviter, type(inviter))
            if invited_email != email:
                messages.error(request,
                               _("Can not register with this email address, use password or related social media."))
                return redirect('main:homepage')
            print(userinfo)
            user = User.objects.create(
                username=email.split('@')[0],
                email=email,
                first_name=userinfo.get('given_name'),
                last_name=userinfo.get('family_name')
            )
            login(request, user)

    return redirect('main:homepage')


class LoginPage(auth_views.LoginView):
    """
    Session-based login.
    Note: It will redirect to homepage after a successful login.
    You can change this in settings --> LOGIN_REDIRECT_URL
    """
    template_name = "accounts/login.html"


class LogoutView(auth_views.LogoutView):
    """
    Session-based logout.
    Note: It will redirect to login page after a successful logout.
    You can change this in settings --> LOGOUT_REDIRECT_URL
    """
    pass


class RegisterView(generic.View):
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
            else:
                return render(request, 'accounts/register.html', context={'form': form, 'inviter': invite_obj.inviter})
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

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        tag_exists = TagAssignment.objects.filter(giver=self.request.user).exists()
        if not tag_exists:
            context['tag_form'] = TagForm()
        return context


class SetInviterTagView(LoginRequiredMixin, generic.View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        tag_form = TagForm(request.POST)
        profile_form = ProfileForm(instance=profile)
        context = {
            'form': profile_form
        }
        if tag_form.is_valid():
            for tag in tag_form.cleaned_data['comma_separated_tags'].split(","):
                TagAssignment.objects.create(
                    tag=get_tag_by_name(tag),
                    receiver=get_inviter(self.request.user.email),
                    giver=self.request.user
                )
            return redirect("accounts:profile")
        else:
            context.update({'tag_form': tag_form})

        return render(request, 'accounts/profile_update.html', context)


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
