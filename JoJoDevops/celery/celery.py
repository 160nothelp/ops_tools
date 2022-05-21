import os
from celery import Celery, platforms
from kombu import Exchange, Queue

from JoJoDevops.celery.celery_routes import CELERY_ROUTES
from JoJoDevops.celery.celery_crontab import CELERY_BEAT_SCHEDULE


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JoJoDevops.settings')
app = Celery("MyCelery")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_transport_options = {'visibility_timeout': 86400}
platforms.C_FORCE_ROOT = True


CELERY_QUEUES = (
    Queue("default", Exchange("default", type='direct'), routing_key="default"),
    Queue("for_task_crontab", Exchange("for_task_crontab", type='direct'), routing_key="for_task_crontab"),
    Queue("for_task_run", Exchange("for_task_run", type='direct'), routing_key="for_task_run"),
)


CELERY_ROUTES = CELERY_ROUTES

app.conf.update(CELERY_QUEUES=CELERY_QUEUES, CELERY_ROUTES=CELERY_ROUTES)

app.conf.update(
    CELERY_BEAT_SCHEDULE=CELERY_BEAT_SCHEDULE
)
