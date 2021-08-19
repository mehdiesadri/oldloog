from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from discovery.models import TagAssignment


def profile_required(function):
    """
    We can put this decorator before @login_required and
    check if the user can continue or should complete its profile first.
    """

    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        profile = request.user.profile
        tag_exists = TagAssignment.objects.filter(giver=request.user).exists()
        if profile.is_completed and tag_exists:
            return function(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, _("Please complete your profile."))
            return redirect("accounts:profile_update")

    return wrap
