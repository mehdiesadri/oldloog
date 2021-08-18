from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from discovery.models import TagAssignment


class ProfileRequiredMixin:
    """Verify that the current user has a complete profile."""

    def dispatch(self, request, *args, **kwargs):
        profile = request.user.profile
        tag_exists = TagAssignment.objects.filter(giver=request.user).exists()
        if not profile.is_completed or not tag_exists:
            messages.add_message(request, messages.ERROR, _("Please complete your profile or tag your inviter."))
            return redirect("accounts:profile_update")
        return super().dispatch(request, *args, **kwargs)
