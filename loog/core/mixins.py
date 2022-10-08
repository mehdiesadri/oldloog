from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from discovery.models import TagAssignment


class ProfileRequiredMixin(LoginRequiredMixin):
    """
    Verify that the current user has a complete profile.
    """

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if response.status_code == 302:
            return response

        if request.user.is_superuser:
            return response
        
        profile = request.user.profile
        tag_exists = TagAssignment.objects.filter(giver=request.user).exists()
        
        if not profile.is_completed or not tag_exists:
            messages.error(request, _("Please complete your profile or tag your inviter."))
            return redirect("accounts:profile_update")
        return response
