from django.conf import settings
from nexmomessage import NexmoMessage


def send_sms_message(to, message):
    """Shortcut to send a sms using libnexmo api.

    Usage:

    >>> send_message('+33612345678', 'My sms message body')
    """
    # TODO: Pull 'from' value from db
    params = {
        'api_key': settings.NEXMO_USERNAME,
        'api_secret': settings.NEXMO_PASSWORD,
        'type': 'text',
        'from': '19189620405',
        'to': to,
        'text': message.encode('utf-8'),
    }
    sms = NexmoMessage(params)
    response = sms.send_request()
    return response
