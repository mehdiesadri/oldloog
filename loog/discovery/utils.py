from django.db.models import Count

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


def get_tag_counts_in_assignments(assignments) -> dict:
    annotated_tags = assignments.values_list('tag__name').annotate(total=Count('tag')).order_by('total')
    tag_counts = {}
    for tag_name, tag_count in annotated_tags:
        tag_counts[tag_name] = tag_count
    return tag_counts
