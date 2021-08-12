from django.db.models import Count


def get_tag_counts_in_assignments(assignments) -> dict:
    annotated_tags = assignments.values_list('tag__name').annotate(total=Count('tag')).order_by('-total')
    tag_counts = {}
    for tag_name, tag_count in annotated_tags:
        tag_counts[tag_name] = tag_count
    return tag_counts
