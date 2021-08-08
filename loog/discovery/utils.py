from .models import TagAssignment


def check_profile(profile):
    """
    A profile is complete when it has all fields and gave some tags.
    """
    user = profile.user
    if user.is_staff or user.is_superuser:
        return True
    tag_exists = TagAssignment.objects.filter(giver=user).exists()
    if tag_exists and profile.is_completed:
        return True
    return False
