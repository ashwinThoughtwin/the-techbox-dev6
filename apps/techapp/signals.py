from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from the_tech_box.settings import EMAIL_HOST_USER
from .models import TechItem


@receiver(post_save, sender=TechItem)
def send_new_techitem_notification_email(sender, instance, created, **kwargs):
    if created:
        item_name = instance.item_name
        item_description = instance.item_description
        subject = 'NAME: {0}, DESCRIPTION: {1},'.format(item_name, item_description)
        message = 'A New Tech Item is Created!\n'
        message += 'NAME: ' + item_name + '\n' + 'DESCRIPTION: ' \
                   + item_description + '\n'
        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            ['rishirajsingh.thoughtwin@gmail.com', ],
            fail_silently=False,
        )
