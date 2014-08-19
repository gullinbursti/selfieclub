from django.conf.urls import patterns, url


urlpatterns = patterns(
    'messaging.views',
    url(r'^nexmo/callback/$', 'callback', name='nexmo_callback'),
)
