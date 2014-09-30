from __future__ import absolute_import

from celery import Celery
from django.conf import settings
import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

if 'SELFIECLUB_CONFIG_DIR' in os.environ:
    CONFIG_DIR = os.environ.get('SELFIECLUB_CONFIG_DIR')
else:
    CONFIG_DIR = os.path.join(os.path.dirname(BASE_DIR), 'selfieclub-config')

sys.path.append(CONFIG_DIR)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selfieclub.settings')

# TODO - Investigate 'invalid-name' on 'app'.  Might be required?
app = Celery('selfieclub')  # pylint: disable=invalid-name

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    # TODO - Switch to logging, print is a bad idea!
    # superfluous-parens - py3 compatability
    print('Request: {0!r}'.format(self.request))  # noqa pylint: disable=superfluous-parens
