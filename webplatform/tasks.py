from django.core.mail import send_mail
from celery import shared_task

@shared_task
def send_mail_with_celery(subject, message, user):
    send_mail(
        subject=subject,
        message=message+user+'.',
        from_email='web.bot@mealhippo.com',
        recipient_list=['hello@mealhippo.com'],
        fail_silently=True,
    )
    return None
