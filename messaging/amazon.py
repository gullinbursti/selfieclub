"""Send messages via the Amazon SNS service."""

import boto
from boto import sns
from django.conf import settings
import json
import re

# APNS for production. APNS_SANDBOX for dev
ENVIRONMENT = settings.AMAZON_SNS_ENV
# One for dev, another for production
PLATFORM_ARN = settings.AMAZON_SNS_ARN
AMAZONSNS = sns.SNSConnection(settings.AWS_CREDENTIALS['key'],
                              settings.AWS_CREDENTIALS['secret'])


def send_push_message(device_token, message_text, payload=None):
    """Shortcut to send a push message using Amazon's SNS API."""
    response = None
    # idempotent call to create/retrieve device_arn for this token
    try:
        d_rspnse = AMAZONSNS.create_platform_endpoint(PLATFORM_ARN,
                                                      device_token, None,
                                                      {u'Token': device_token,
                                                       u'Enabled': True})
    except boto.exception.BotoServerError as exception:
        match = re.match(".*Endpoint (?P<arn>.*?) already.*",
                         exception.message)
        AMAZONSNS.delete_endpoint(match.group('arn'))
    d_rspnse = AMAZONSNS.create_platform_endpoint(
        PLATFORM_ARN, device_token, None,
        {u'Token': device_token, u'Enabled': True})
    if 'CreatePlatformEndpointResponse' in d_rspnse:
        device_arn = d_rspnse['CreatePlatformEndpointResponse'][
            'CreatePlatformEndpointResult']['EndpointArn']
        apns_dict = {'aps': {'alert': message_text, 'sound': 'default'}}
        for key, value in payload.items():
            apns_dict['aps'][key] = value
        apns_string = json.dumps(apns_dict, ensure_ascii=False)
        message = {'default': message_text, ENVIRONMENT: apns_string}
        message_json = json.dumps(message, ensure_ascii=False)

        response = AMAZONSNS.publish(
            message=message_json,
            target_arn=device_arn,
            message_structure='json')
    return response
