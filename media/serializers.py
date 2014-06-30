from rest_framework import serializers
from drf_compound_fields.fields import ListField


class UploadInstructionsRequestSerializer(serializers.Serializer):
    club_id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=True)
    content_type = serializers.CharField(required=True, max_length=100)
    file_name = serializers.CharField(required=True, max_length=100)
    size = serializers.IntegerField(required=True)


class KeyValuePairSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    value = serializers.CharField(required=True)


class HttpPostMultipartFormSerializer(serializers.Serializer):
    header_fields = KeyValuePairSerializer(many=True)
    action = serializers.URLField(required=True)
    upload_form_field = serializers.CharField(required=True, max_length=100)
    form_fields = KeyValuePairSerializer(many=True)


class UploadInstructionsResponseSerializer(serializers.Serializer):
    http_post_multipart_form = HttpPostMultipartFormSerializer(required=True)
    callbacks = ListField(serializers.URLField())
