from django.db.models import Q, Sum
from django.forms import widgets
from rest_framework import serializers
from status import models


class StatusUpdate(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    class Meta(object):
        # pylint: disable=too-few-public-methods
        model = models.StatusUpdate
        fields = ('id', 'creator_id', 'is_private', 'votes', 'added')


class ExpandedStatusUpdate(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    owner_member_id = serializers.IntegerField(source='creator_id')
    img = serializers.CharField(source='creator_img')
    text = serializers.CharField(source='subject')
    emotions = serializers.CharField(source='emotions', read_only=True)
    net_vote_score = serializers.IntegerField(read_only=True, source='*')

    def transform_net_vote_score(self, obj, value):
        queryset = models.StatusUpdateVoter.objects
        if not obj.parent_id:
            queryset = queryset.filter(
                Q(status_update=obj.id)
                | Q(status_update__parent_id=obj.id))
        else:
            queryset = queryset.filter(status_update=obj.id)
        result = queryset.aggregate(net_vote_score=Sum('vote'))
        return result['net_vote_score']

    class Meta(object):
        # pylint: disable=too-few-public-methods
        model = models.StatusUpdate
        fields = ('id', 'owner_member_id', 'img', 'text', 'emotions',
                  'net_vote_score', 'added', 'updated')


class StatusUpdateViewerSerializer(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
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


class StatusUpdateVoterSerializer(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    member_id = serializers.IntegerField(
        widget=widgets.TextInput,
        source='member_id',
        help_text='Enter member_id.')
    member = serializers.SlugRelatedField(read_only=True,
                                          slug_field='name')
    vote = serializers.IntegerField(
        widget=widgets.TextInput,
        source='vote',
        help_text='Enter vote.')
    status_update_id = serializers.IntegerField(
        widget=widgets.TextInput,
        source='status_update_id',
        help_text='This value is ignored in POSTs, pulled from URL.')

    def transform_vote(self, obj, value):
        # pylint: disable=no-self-use, unused-argument
        if value == -1:
            return 'down'
        else:
            return 'up'

    class Meta(object):
        # pylint: disable=too-few-public-methods
        model = models.StatusUpdateVoter
        fields = ('member_id', 'member', 'vote', 'status_update_id')
