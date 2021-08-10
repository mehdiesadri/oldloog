"""
In this module we put all selects, filters, and fetches from the database.
--> read-only!
"""
import logging

from .utils import get_tag_counts_in_assignments
from .models import TagAssignment, Tag

logger = logging.getLogger(__name__)


def is_there_any_tag_assignment(giver, receiver) -> bool:
    """
    Gets the giver and receiver user instances and says is there any tag assignment or not.

    Args:
        giver: The user instance of the person who gave the tag.
        receiver: The user instance of the person who received the tag.

    Returns:
        A boolean indicating that there is a tag assignment or not.
    """

    return TagAssignment.objects.filter(giver=giver, receiver=receiver).exists()


def get_tag_count(**kwargs) -> dict:
    """
    Gets an user instance and returns a dictionary of given tags.

    Args:
        kwargs: Filter parameter for TagAssignment, such as giver and receiver

    Returns:
       A dictionary of tags which keys are tag names and values are its count.

    Example:
        {'python': 2, 'django': 2, 'web': 2, 'tehran': 2, 'iran': 2}
    """
    assignments = TagAssignment.objects.filter(**kwargs)
    return get_tag_counts_in_assignments(assignments)


def get_tag_by_name(name: str):
    """
    Gets or creates a Tag object by its name.

    Args:
        name: A string value of a tag name.

    Returns:
        Related Tag object.
    """
    return Tag.objects.get_or_create(name=name)[0]
