from .models import TagAssignment


def check_profile(profile):
    tag_exists = TagAssignment.objects.filter(giver=profile.user).exists()
    if tag_exists and profile.is_completed:
        return True
    return False
