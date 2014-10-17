from status import models
from django.forms import widgets
from rest_framework import serializers


class StatusUpdate(serializers.ModelSerializer):
    class Meta(object):
        # pylint: disable=too-few-public-methods
        model = models.StatusUpdate
        fields = ('id', 'creator_id', 'is_private', 'votes', 'added')


class StatusUpdateViewerSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(
        widget=widgets.TextInput,
        source='member_id',
        help_text='Enter member_id.')
    status_update_id = serializers.IntegerField(
        widget=widgets.TextInput,
        source='status_update_id',
        help_text='This value is ignored in POSTs, pulled from URL.')

    class Meta(object):
        # pylint: disable=too-few-public-methods
        model = models.StatusUpdateViewer
        fields = ('member_id', 'status_update_id')
