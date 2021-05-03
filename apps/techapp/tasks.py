from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from celery import shared_task
from the_tech_box.settings import EMAIL_HOST_USER

# from .email import send_remainder_email

logger = get_task_logger(__name__)


@shared_task()
def send_email_task(subject, message, email):
    logger.info("Sent confirmation email")
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [email, ],
        fail_silently=False,
    )


@shared_task()
def send_remember_task(subject_remember, message_remember, email):
    logger.info("Sent remember email")
    send_mail(
        subject_remember,
        message_remember,
        EMAIL_HOST_USER,
        [email, ],
        fail_silently=False,
    )
