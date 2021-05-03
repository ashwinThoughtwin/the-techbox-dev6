from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_remainder_email(employee_name, tech_item, end_date, email):  # pragma: no cover
    context = {
        'employee_name': employee_name,
        'tech_item': tech_item,
        'end_date': end_date,
    }

    email_subject = 'Remainder for your borrow item'
    email_body = render_to_string('email_message.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)
