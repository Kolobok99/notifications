import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
app = Celery('conf')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.timezone = settings.TIME_ZONE

app.autodiscover_tasks()



