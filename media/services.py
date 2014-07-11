from django.conf import settings
from hashlib import sha1
from rest_framework.renderers import JSONRenderer
import base64
import binascii
import datetime
import hmac


class UploadInstructionsService(object):

    UPLOAD_FORM_FIELD = 'file'
    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    def process(self, member_id, content_type, file_name, size, club_id=None):
        # Pull in configuration information
        aws_key = settings.AWS_CREDENTIALS['key']
        aws_secret = settings.AWS_CREDENTIALS['secret']
        aws_url = settings.AWS_S3_DIRECT_CLIENT_UPLOAD['url']
        acl = settings.AWS_S3_DIRECT_CLIENT_UPLOAD['acl']
        bucket = settings.AWS_S3_DIRECT_CLIENT_UPLOAD['bucket']
        expiry_minutes = settings.AWS_S3_DIRECT_CLIENT_UPLOAD['expiry_minutes']

        # Prepare
        expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiry_minutes)
        expiry_iso = expiry.strftime(self.DATETIME_FORMAT)

        policy = {
            'expiration': expiry_iso,
            'conditions': [
                {'bucket': bucket},
                {'key': file_name},
                {'acl': acl},
                {'Content-Type': content_type},
                ['content-length-range', size, size]
            ]
        }

        # Build and sign policy
        policy_json = JSONRenderer().render(policy)
        policy_base64 = base64.b64encode(policy_json)
        policy_sig = hmac.new(aws_secret, policy_base64, sha1)
        policy_sig_base64 = binascii.b2a_base64(policy_sig.digest())[:-1]

        response = {
            "http_post_multipart_form": {
                "action": aws_url,
                "header_fields": [],
                "upload_form_field": self.UPLOAD_FORM_FIELD,
                "form_fields": [
                    {"name": "key", "value": file_name},
                    {"name": "acl", "value": acl},
                    {"name": "AWSAccessKeyId", "value": aws_key},
                    {"name": "Content-Type", "value": content_type},
                    {"name": "Policy", "value": policy_base64},
                    {"name": "Signature", "value": policy_sig_base64}
                ]
            },
            "callbacks": [],
        }

        return response
