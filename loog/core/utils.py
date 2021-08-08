from django.core.mail import send_mail


def send_mail_to(subject, message, receivers):
    return send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=receivers,
        fail_silently=False
    )
