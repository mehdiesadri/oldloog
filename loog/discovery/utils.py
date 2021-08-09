import operator

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


def get_tag_counts_in_assignments(assignments):
    # TODO: is there a better approach
    tags = {}
    for assignment in assignments:
        tag = assignment.tag.name
        if tag not in tags:
            tags[tag] = 0
        tags[tag] = tags[tag] + 1
    sorted_tags = dict(sorted(tags.items(), key=operator.itemgetter(1), reverse=True))
    return sorted_tags
