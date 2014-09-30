"""Send messages via the Nexmo SMS service."""

from django.db.models import F
from django.conf import settings
from nexmomessage import NexmoMessage
from messaging import models
import requests


def send_sms_message(recipient, message, mtype='text'):
    """Shortcut to send sms using libnexmo api and a pool of source numbers."""
    params = {
        'api_key': settings.NEXMO_USERNAME,
        'api_secret': settings.NEXMO_PASSWORD,
        'type': mtype,
        'from': getSourceNumber(),
        'to': recipient,
        'text': message.encode('utf-8'),
    }
    sms = NexmoMessage(params)
    response = sms.send_request()
    return response


def send_unicode_message(recipient, message):
    """Shortcut to send sms using libnexmo api and a pool of source numbers."""
    rest_url = 'http://rest.nexmo.com/sms/xml'
    payload = {'type': 'unicode',
               'api_key': settings.NEXMO_USERNAME,
               'api_secret': settings.NEXMO_PASSWORD,
               'from': getSourceNumber(),
               'to': recipient,
               'text': message.decode('unicode_escape')}
    response = requests.get(rest_url, params=payload)
    return response


def getSourceNumber():
    """Helper to rotate through pool of SMS source numbers."""
    # TODO: Should we cache this count?
    pool_size = models.SourceNumber.objects.count()
    # TODO: Make one atomic query. Had some trouble returning the value
    models.PoolCounter.objects.filter(
        name='NEXMO_PHONE_SEQ').update(counter=F('counter')+1)
    source_pool = models.PoolCounter.objects.get(name='NEXMO_PHONE_SEQ')
    key = (source_pool.counter % pool_size) + 1
    source = models.SourceNumber.objects.get(pk=key)
    return source.phone_number
