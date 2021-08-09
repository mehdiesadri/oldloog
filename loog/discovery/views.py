from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from core.mixins import ProfileRequiredMixin
from .forms import InitialTagsInputForm, InviteForm, ProfileForm, InviteeTagForm
from .models import TagAssignment
from .selectors import get_invites_count, get_inviter, is_there_any_tag_assignment, get_tag_count, get_tag_by_name


class IndexPage(ProfileRequiredMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = 'discovery/index.html'


class InvitePage(SuccessMessageMixin, ProfileRequiredMixin, LoginRequiredMixin, generic.CreateView):
    template_name = 'discovery/invite.html'
    form_class = InviteForm
    success_url = reverse_lazy("discovery:invite")
    success_message = _("You friend successfully invited. We will send him/her an invitation email.")

    def form_valid(self, form):
        invited = form.save(commit=False)
        invited.inviter = self.request.user
        invited.save()
        return super(InvitePage, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(InvitePage, self).get_context_data(**kwargs)
        context['length'] = get_invites_count(self.request.user)
        return context


class ProfileUpdatePage(SuccessMessageMixin, LoginRequiredMixin, generic.FormView):
    template_name = "discovery/profile_update.html"
    form_class = ProfileForm
    success_url = reverse_lazy("discovery:profile")
    success_message = _("You profile successfully updated.")

    def get_form(self, form_class=ProfileForm):
        profile = self.request.user.profile
        return form_class(instance=profile, **self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(ProfileUpdatePage, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdatePage, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user.is_staff:
            return context

        inviter = get_inviter(self.request.user.email)
        context["has_tag_form"] = not is_there_any_tag_assignment(giver=self.request.user, receiver=inviter)
        context["inviter"] = inviter
        context["tag_form"] = InviteeTagForm(initial={'user': inviter.id})

        return context


class InviteeTagPage(SuccessMessageMixin, LoginRequiredMixin, generic.FormView):
    template_name = "discovery/profile_update.html"
    form_class = InviteeTagForm
    success_url = reverse_lazy("discovery:profile_update")
    success_message = _("Tags updated successfully")

    def form_valid(self, form):
        with transaction.atomic():
            for tag in form.cleaned_data.get("comma_separated_tags").split(","):
                TagAssignment.objects.create(
                    tag=get_tag_by_name(tag),
                    receiver_id=form.cleaned_data.get("user"),
                    giver=self.request.user
                )
        return super(InviteeTagPage, self).form_valid(form)


class ProfilePage(ProfileRequiredMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = "discovery/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfilePage, self).get_context_data(**kwargs)

        user = self.request.user
        profile = user.profile
        tags = {"gived": get_tag_count(giver=user), "recieved": get_tag_count(receiver=user)}
        context["tags"] = tags
        context["profile"] = profile
        return context


def discover(request, username, query):
    user = User.objects.filter(username=username).first()
    numGivedTags = get_tag_count(giver=user).keys()

    if len(numGivedTags) < 5:
        initial_tags_form = InitialTagsInputForm()
        return render(
            request=request,
            template_name="discovery/initial_tags.html",
            context={"initial_tags_form": initial_tags_form},
        )
    else:
        matchingAssignments = TagAssignment.objects.select_related("tag").filter(
            tag__value__icontains=str(query)
        )
        matchingProfiles = {}

        for matchingAssignment in matchingAssignments:
            reciever = matchingAssignment.reciever
            if reciever not in matchingProfiles:
                matchingProfiles[reciever] = 0
            matchingProfiles[reciever] = matchingProfiles[reciever] + 1

        return redirect("/chat", matchingProfiles=matchingProfiles)
