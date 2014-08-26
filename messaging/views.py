import messaging
from messaging import tasks
from django.http import HttpResponse


def callback(request):
    """Callback URL for Nexmo."""
    status_id = None
    if 'status' in request.GET:
        status_id = request.GET.get('status')
    error_id = None
    if 'err-code' in request.GET:
        error_id = int(request.GET.get('err-code'))
    response_id = request.GET.get('messageId')
    response_source = None
    if 'msisdn' in request.GET:
        response_source = request.GET.get('msisdn')
    response_carrier = None
    if 'network-code' in request.GET:
        response_carrier = request.GET.get('network-code')
    response_text = request.GET.get('text').strip()
    response_timestamp = request.GET.get('message-timestamp')
    response_destination = request.GET.get('to')

    callback = messaging.models.Callback(
        message_id=response_id,
        status_id=status_id,
        error_id=error_id,
        source_number=response_source,
        source_network=response_carrier,
        destination_number=response_destination,
        text=response_text,
        callback_timestamp=response_timestamp
    )
    callback.save()

    if response_source and (response_text == 'YES'):
        tasks.send_sms_thanks.delay(response_source)

    # Nexmo expects a 200 response code
    return HttpResponse('')
