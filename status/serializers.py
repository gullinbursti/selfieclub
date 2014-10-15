from status import models
from rest_framework import serializers


class StatusUpdate(serializers.ModelSerializer):
    class Meta(object):
        # pylint: disable=too-few-public-methods
        model = models.StatusUpdate
        fields = ('id', 'creator_id', 'is_private', 'votes', 'added')


class StatusUpdateViewerSerializer(serializers.ModelSerializer):
    class Meta(object):
        # pylint: disable=too-few-public-methods
        model = models.StatusUpdateViewer
        fields = ('member',)
