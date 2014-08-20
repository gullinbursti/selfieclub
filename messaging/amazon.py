from django.conf import settings
import boto
from boto import sns


sns = boto.sns.SNSConnection(settings.AWS_CREDENTIALS['key'],
                             settings.AWS_CREDENTIALS['secret'])


def send_push_message(to, message):
    """Shortcut to send a push message using Amazon's SNS API

    Usage:

    >>> send_push_message(device_arn, 'My push message text')
    """
    arn = to
    plain_text_message = message
    response = sns.publish(message=plain_text_message, target_arn=arn)
    return response
