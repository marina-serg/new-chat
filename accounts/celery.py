import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_channels_chat.settings')
app = Celery('accounts', broker_connection_retry=False,
             broker_connection_retry_on_startup=True, )
app.config_from_object('django.conf:settings')
broker_connection_retry = False

app.autodiscover_tasks()
