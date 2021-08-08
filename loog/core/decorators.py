from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from discovery.utils import check_profile


def profile_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        profile = request.user.profile
        if check_profile(profile):
            return function(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, "Please complete your profile.")
            return redirect("discovery:profile_complete")
    return wrap
