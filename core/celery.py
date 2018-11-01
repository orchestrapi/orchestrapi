from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

CELERY_SETTINGS = os.environ.get('CELERY_SETTINGS', 'core.settings.base')

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', CELERY_SETTINGS)

app = Celery('core')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))