from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


def profile_required(function):
    """
    We can put this decorator before @login_required and
    check if the user can continue or should complete its profile first.
    """

    @wraps(function)
    def wrap(request, *args, **kwargs):
        profile = request.user.profile
        if profile.is_completed:
            return function(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, _("Please complete your profile."))
            return redirect("accounts:profile_update")

    return wrap
