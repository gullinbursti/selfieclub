import boto
from boto import sns
from django.conf import settings
import json
import re

# APNS for production. APNS_SANDBOX for dev
environment = settings.AMAZON_SNS_ENV
# One for dev, another for production
platform_arn = settings.AMAZON_SNS_ARN
amazonsns = sns.SNSConnection(settings.AWS_CREDENTIALS['key'],
                              settings.AWS_CREDENTIALS['secret'])


def send_push_message(device_token, message_text, payload=None):
    """Shortcut to send a push message using Amazon's SNS API

    Usage:

    >>> send_push_message(device_token, 'My push message text')
    """
    response = None
    # idempotent call to create/retrieve deviceArn for this token
    try:
        dResponse = amazonsns.create_platform_endpoint(
            platform_arn, device_token, None,
            {u'Token': device_token, u'Enabled': True})
    except boto.exception.BotoServerError, e:
        match = re.match(".*Endpoint (?P<arn>.*?) already.*",
                         e.message)
        amazonsns.delete_endpoint(match.group('arn'))
    dResponse = amazonsns.create_platform_endpoint(
        platform_arn, device_token, None,
        {u'Token': device_token, u'Enabled': True})
    if 'CreatePlatformEndpointResponse' in dResponse:
        deviceArn = dResponse[
            'CreatePlatformEndpointResponse'][
            'CreatePlatformEndpointResult'][
            'EndpointArn']
        apns_dict = {'aps': {'alert': message_text, 'sound': 'default'}}
        for key, value in payload.items():
            apns_dict['aps'][key] = value
        apns_string = json.dumps(apns_dict, ensure_ascii=False)
        message = {'default': message_text, environment: apns_string}
        messageJSON = json.dumps(message, ensure_ascii=False)

        response = amazonsns.publish(
            message=messageJSON,
            target_arn=deviceArn,
            message_structure='json')
    return response
