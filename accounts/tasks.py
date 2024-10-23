from django.core.mail import send_mail

from django_channels_chat.settings import EMAIL_HOST_USER
from .celery import app


@app.task
def send_reset_email(subject, message, recipient_list):
    send_mail(subject, message, EMAIL_HOST_USER, recipient_list)
