from django.conf import settings
from boto import sns
import json


amazonsns = sns.SNSConnection(settings.AWS_CREDENTIALS['key'],
                              settings.AWS_CREDENTIALS['secret'])
arn = settings.AMAZON_SNS_ARN


def send_push_message(to, message):
    """Shortcut to send a push message using Amazon's SNS API

    Usage:

    >>> send_push_message(device_arn, 'My push message text')
    """
    apns_dict = {'aps': {'alert': message, 'sound': 'default'}}
    apns_string = json.dumps(apns_dict, ensure_ascii=False)
    message = {'default': 'default message', 'APNS_SANDBOX': apns_string}
    messageJSON = json.dumps(message, ensure_ascii=False)

    response = amazonsns.publish(
        message=messageJSON, target_arn=arn, message_structure='json')
    return response
