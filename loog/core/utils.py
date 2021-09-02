from django.core.mail import send_mail


def send_mail_to(subject: str, message: str, receivers: list):
    """
    Sends email using the configurations in the settings.

    Args:
        subject: The subject of the email.
        message: The body of the email.
        receivers: List of email addresses.
    
    Returns:
        An integer number, 1 is success.
    """
    return send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=receivers,
        fail_silently=False
    )
