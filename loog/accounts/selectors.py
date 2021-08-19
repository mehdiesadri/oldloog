import logging

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from accounts.models import InvitedUser


def get_invites_count(inviter) -> int:
    """
    Gets an user instance and returns the number of friends invited by him/her.

    Args:
        inviter: A django user instance.

    Returns:
        The number of people who invited by this user.
    """
    return InvitedUser.objects.filter(inviter=inviter).count()


def get_inviter(user_email: str):
    """
    Gets an user email and returns the user instance who invited him/her.

    Args:
        user_email: The string value of an email address.

    Returns:
        The user instance who invited the given email address.

    Raises:
        DoesNotExists: If no one invited the giver email address.
    """
    invite_instance = InvitedUser.objects.filter(email=user_email, is_registered=True).first()
    if invite_instance:
        return invite_instance.inviter
    logging.error(f"No user invited the email address: {user_email}.")
    raise InvitedUser.DoesNotExist()


def get_invite_obj_from_url(uidb64_invite_id: str):
    try:
        invite_id = force_text(urlsafe_base64_decode(uidb64_invite_id))
        invite_obj = InvitedUser.objects.get(pk=invite_id)
    except (TypeError, ValueError, OverflowError, InvitedUser.DoesNotExist):
        invite_obj = None
    return invite_obj


def get_invite_obj_from_inviter_username(username: str, invited_email: str):
    try:
        invited_obj = InvitedUser.objects.get(inviter__username=username, email=invited_email)
    except (TypeError, ValueError, OverflowError, InvitedUser.DoesNotExist):
        invited_obj = None
    return invited_obj
