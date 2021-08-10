from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from core.mixins import ProfileRequiredMixin
from .forms import InitialTagsInputForm, InviteeTagForm, InviteForm
from .models import TagAssignment
from .selectors import get_invites_count, get_tag_count, get_tag_by_name


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


class InviteeTagPage(SuccessMessageMixin, LoginRequiredMixin, generic.FormView):
    template_name = "discovery/profile_update.html"
    form_class = InviteeTagForm
    success_url = reverse_lazy("accounts:profile_update")
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
