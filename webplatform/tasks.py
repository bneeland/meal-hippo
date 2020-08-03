from django.core.mail import send_mail
from celery import shared_task
from django.utils import timezone

@shared_task
def send_mail_with_celery(subject, message, recipient_list, html_message):
    send_mail(
        subject=subject,
        message=message,
        from_email='hello@mealhippo.com',
        recipient_list=recipient_list,
        fail_silently=True,
        html_message=html_message,
    )
    return None
