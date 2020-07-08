from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
# set the default Django settings module for the 'celery' program.
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HttpRunnerManager.settings')

app = Celery('HttpRunnerManager',backend="redis",broker=settings.BROKER_URL)

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
