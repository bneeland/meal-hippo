from django.core.mail import send_mail
from celery import shared_task
from django.utils import timezone

@shared_task
def send_mail_with_celery(subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email='web.bot@mealhippo.com',
        recipient_list=['hello@protonmail.com'],
        fail_silently=True,
    )
    return None
