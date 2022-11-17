import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
app = Celery('conf')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.timezone = settings.TIME_ZONE

app.autodiscover_tasks()

app.conf.beat_schedule = {
	'send-statistics-to-admin-every_day': {
		'task': "polls.tasks.task_send_statistics_to_admin",
		'schedule': crontab(hour=23, minute=50),
	},
}


