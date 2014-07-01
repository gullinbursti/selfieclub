"""
WSGI config for selfieclub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
#site.addsitedir('/var/deploy/selfieclub/.virtualenv/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/deploy/selfieclub')
#sys.path.append('/var/deploy/selfieclub/selfieclub')





activate_this = os.path.dirname(__file__) + '/../.virtualenv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "selfieclub.settings")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "selfieclub.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
