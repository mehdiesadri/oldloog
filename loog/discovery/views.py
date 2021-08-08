import operator

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy

from core.decorators import profile_required
from .forms import InitialTagsInputForm, InviteForm, ProfileForm
from .models import Profile, Tag, TagAssignment
from django.contrib.auth.models import User


@profile_required
@login_required
def index(request):
    return HttpResponse("Hello, world. You're at the discovery index.")


class InvitePage(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    template_name = 'discovery/invite.html'
    form_class = InviteForm
    success_url = reverse_lazy("discovery:invite")
    success_message = _("You friend successfully invited. We will send him/her an invitation email.")

    def form_valid(self, form):
        invited = form.save(commit=False)
        invited.inviter = self.request.user
        invited.save()
        return super(InvitePage, self).form_valid(form)


class ProfileCompletePage(SuccessMessageMixin, LoginRequiredMixin, generic.FormView):
    template_name = "discovery/profile_complete.html"
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy("discovery:profile")
    success_message = _("You profile successfully updated.")
    # TODO: Add tag for inviter

    def get_form(self, form_class=ProfileForm):
        profile = self.request.user.profile
        return form_class(instance=profile, **self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(ProfileCompletePage, self).form_valid(form)


def get_profile(request):
    user = request.user

    profile = Profile.objects.filter(user=user).first()
    tags = {"gived": getGivedTags(user), "recieved": getRecievedTags(user)}
    return render(
        request=request, template_name="discovery/profile.html", context={"tags": tags, "profile": profile}
    )


def set_initial_tags(request, username):
    user = User.objects.filter(username=username).first()
    profile = Profile.objects.filter(user=user).first()

    if request.method == "POST":
        form = InitialTagsInputForm(request.POST)
        if form.is_valid():
            target_username = request.POST["user"]
            target_user = User.objects.filter(username=target_username).first()
            target_profile = Profile.objects.filter(user=target_user).first()
            tags = [
                get_tag(request.POST["tag1"]),
                get_tag(request.POST["tag2"]),
                get_tag(request.POST["tag3"]),
                get_tag(request.POST["tag4"]),
                get_tag(request.POST["tag5"]),
            ]
            for tag in tags:
                usertag = TagAssignment(
                    tag=tag, giver=profile, reciever=target_profile, location="US"
                )
                usertag.save()
    return redirect("main:homepage")


def discover(request, username, query):
    user = User.objects.filter(username=username).first()
    profile = Profile.objects.filter(user=user).first()
    numGivedTags = getGivedTags(profile).keys()

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


def getGivedTags(profile):
    assignments = TagAssignment.objects.filter(giver=profile)
    return processTags(assignments)


def getRecievedTags(profile):
    assignments = TagAssignment.objects.filter(receiver=profile)
    return processTags(assignments)


def processTags(assignments):
    tags = {}
    for assignment in assignments:
        tag = assignment.tag.value
        if tag not in tags:
            tags[tag] = 0
        tags[tag] = tags[tag] + 1
    sorted_tags = dict(sorted(tags.items(), key=operator.itemgetter(1), reverse=True))
    return sorted_tags


def get_tag(tag_str):
    tag = Tag.objects.filter(value=tag_str).first()
    if tag is None:
        tag = Tag(value=tag_str, type=1)
        tag.save()
    return tag
