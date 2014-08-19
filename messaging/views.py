from django.http import HttpResponse
from .error_messages import (NEXMO_STATUSES, UNKNOWN_STATUS,
                             NEXMO_MESSAGES, UNKNOWN_MESSAGE)
import logging


logger = logging.getLogger('nexmo')


def callback(request):
    """Callback URL for Nexmo."""
    status_id = None
    status_msg = None
    if 'status' in request.GET:
        status_id = request.GET.get('status')
        status_msg = NEXMO_STATUSES.get(status_id, UNKNOWN_STATUS)
    error_id = None
    error_msg = None
    if 'err-code' in request.GET:
        error_id = int(request.GET.get('err-code'))
        error_msg = NEXMO_MESSAGES.get(error_id, UNKNOWN_MESSAGE)
    response_id = request.GET.get('messageId')
    response_source = None
    if 'msisdn' in request.GET:
        response_source = request.GET.get('msisdn')
    response_carrier = None
    if 'network-code' in request.GET:
        response_carrier = request.GET.get('network-code')
    response_text = request.GET.get('text')
    response_timestamp = request.GET.get('message-timestamp')
    response_destination = request.GET.get('to')

    logger.info(u'Nexmo callback: Sms = {}, Status = {}, Error = {}, '.format(
        response_id, status_msg, error_msg) +
        u'from={}@carrier={}->to={}@at={}: text={}'.format(
            response_source, response_carrier, response_destination,
            response_timestamp, response_text))

    # Nexmo expects a 200 response code
    return HttpResponse('')
