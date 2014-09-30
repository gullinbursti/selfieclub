"""Define inbound URL patterns related to messaging."""
from django.conf.urls import patterns, url


# 'urlpatterns' is required by django
urlpatterns = patterns(  # pylint: disable=invalid-name
    'messaging.views',
    url(r'^nexmo/callback/$', 'callback', name='nexmo_callback'),
)
