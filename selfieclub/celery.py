from __future__ import absolute_import

from celery import Celery
from django.conf import settings
import os
import sys

base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
config_dir = os.path.join(os.path.dirname(base_dir), 'selfieclub-config')
sys.path.append(config_dir)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selfieclub.settings')

app = Celery('selfieclub')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
        print('Request: {0!r}'.format(self.request))
