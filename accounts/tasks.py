from .celery import app
from django.core.mail import send_mail

@app.task
def send_reset_email(subject, message, recipient_list):
    send_mail(subject, message, 'ira.sh2004@yandex.ru', recipient_list)