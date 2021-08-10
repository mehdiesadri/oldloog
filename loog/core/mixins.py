from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class ProfileRequiredMixin:
    """Verify that the current user has a complete profile."""

    def dispatch(self, request, *args, **kwargs):
        profile = request.user.profile
        if not profile.is_completed:
            messages.add_message(request, messages.ERROR, _("Please complete your profile."))
            return redirect("accounts:profile_update")
        return super().dispatch(request, *args, **kwargs)
