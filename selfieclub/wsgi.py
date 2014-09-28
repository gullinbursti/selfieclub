"""
WSGI config for selfieclub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_DIR = os.path.join(os.path.dirname(BASE_DIR), 'selfieclub-config')

# Add the site-packages of the chosen virtualenv to work with
# site.addsitedir('/var/deploy/selfieclub/.virtualenv/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append(BASE_DIR)
sys.path.append(CONFIG_DIR)


ACTIVATE_THIS = os.path.join(BASE_DIR, '.virtualenv', 'bin',
                             'activate_this.py')
execfile(ACTIVATE_THIS, dict(__file__=ACTIVATE_THIS))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "selfieclub.settings")

from django.core.wsgi import get_wsgi_application
# TODO: Might be OK to convert 'application' to all caps?
application = get_wsgi_application()  # pylint: disable=invalid-name
