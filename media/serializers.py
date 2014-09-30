from rest_framework import serializers
from drf_compound_fields.fields import ListField


class UploadInstructionsRequestSerializer(serializers.Serializer):
    # pylint: disable=too-few-public-methods
    club_id = serializers.IntegerField(required=False)
    member_id = serializers.IntegerField(required=True)
    content_type = serializers.CharField(required=True, max_length=100)
    file_name = serializers.CharField(required=True, max_length=100)
    size = serializers.IntegerField(required=True)


class KeyValuePairSerializer(serializers.Serializer):
    # pylint: disable=too-few-public-methods
    name = serializers.CharField(required=True)
    value = serializers.CharField(required=True)


class HttpPostMultipartFormSerializer(serializers.Serializer):
    # pylint: disable=too-few-public-methods
    # TODO # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
    header_fields = KeyValuePairSerializer(many=True)
    action = serializers.URLField(required=True)
    upload_form_field = serializers.CharField(required=True, max_length=100)
    form_fields = KeyValuePairSerializer(many=True)


class UploadInstructionsResponseSerializer(serializers.Serializer):
    # pylint: disable=too-few-public-methods
    # TODO # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
    http_post_multipart_form = HttpPostMultipartFormSerializer(required=True)
    callbacks = ListField(serializers.URLField())
