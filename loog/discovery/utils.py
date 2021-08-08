from .models import TagAssignment


def check_profile(profile):
    """
    A profile is complete when it has all fields and gave some tags.
    """
    tag_exists = TagAssignment.objects.filter(giver=profile.user).exists()
    if tag_exists and profile.is_completed:
        return True
    return False
