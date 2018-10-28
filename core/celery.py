from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from core.settings.secret import CELERY_SETTINGS

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', CELERY_SETTINGS)

app = Celery('core')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))