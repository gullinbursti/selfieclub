from django.db.models import F
from django.conf import settings
from nexmomessage import NexmoMessage
import models
import requests


def send_sms_message(to, message, mtype='text'):
    """Shortcut to send a sms using libnexmo api and a pool of souce numbers

    Usage:

    >>> send_message('+33612345678', 'My sms message body')
    """
    params = {
        'api_key': settings.NEXMO_USERNAME,
        'api_secret': settings.NEXMO_PASSWORD,
        'type': mtype,
        'from': getSourceNumber(),
        'to': to,
        'text': message.encode('utf-8'),
    }
    sms = NexmoMessage(params)
    response = sms.send_request()
    return response


def send_unicode_message(to, message):
    """Shortcut to send a sms using libnexmo api and a pool of souce numbers

    Usage:

    >>> send_message('+33612345678', 'My unicode message body')
    """
    restUrl = 'http://rest.nexmo.com/sms/xml'
    payload = {'type': 'unicode',
               'api_key': settings.NEXMO_USERNAME,
               'api_secret': settings.NEXMO_PASSWORD,
               'from': getSourceNumber(),
               'to': to,
               'text': message.decode('unicode_escape')}
    response = requests.get(restUrl, params=payload)
    return response


def getSourceNumber():
    # TODO: Should we cache this count?
    poolSize = models.SourceNumber.objects.count()
    # TODO: Make one atomic query. Had some trouble returning the value
    models.PoolCounter.objects.filter(
        name='NEXMO_PHONE_SEQ').update(counter=F('counter')+1)
    sourcePool = models.PoolCounter.objects.get(name='NEXMO_PHONE_SEQ')
    key = (sourcePool.counter % poolSize) + 1
    source = models.SourceNumber.objects.get(pk=key)
    return source.phone_number
