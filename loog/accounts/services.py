from django.db import transaction

from discovery.models import TagAssignment
from discovery.selectors import get_tag_by_name


def register_user_with_tags(new_user, invite_obj, new_user_tags: str = None):
    """
    Creates the user objects and sets initial tags.
    # TODO: Is User model a better place for this function?
    """
    with transaction.atomic():
        invite_obj.is_registered = True
        invite_obj.save()

        # Set initial tags: from inviter to new_user
        for tag in invite_obj.comma_separated_tags.split(","):
            TagAssignment.objects.create(
                tag=get_tag_by_name(tag),
                receiver=new_user,
                giver=invite_obj.inviter
            )

        # Set initial tags: from new_user to inviter
        if new_user_tags is not None:
            for tag in new_user_tags.split(","):
                TagAssignment.objects.create(
                    tag=get_tag_by_name(tag),
                    receiver=invite_obj.inviter,
                    giver=new_user
                )
