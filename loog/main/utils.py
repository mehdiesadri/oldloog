from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from discovery.models import InvitedUser


def get_invite_obj_from_url(uidb64_invite_id):
    try:
        invite_id = force_text(urlsafe_base64_decode(uidb64_invite_id))
        invite_obj = InvitedUser.objects.get(pk=invite_id)
    except (TypeError, ValueError, OverflowError, InvitedUser.DoesNotExist):
        invite_obj = None
    return invite_obj
