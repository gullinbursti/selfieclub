from newsfeed_member import models
from rest_framework import serializers
from member import serializers as member_serializers


class NewsfeedType(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    class Meta(object):
        # pylint: disable=too-few-public-methods
        model = models.NewsfeedType
        fields = ('id', 'name', 'description', 'updated', 'created')


class Newsfeed(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    event_type = serializers.SlugRelatedField(
        source='event_type',
        slug_field='name',
        read_only=False)
    member = member_serializers.Member(source='member')  # noqa # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
    club_id = serializers.Field(source='club.id')
    status_update_id = serializers.Field(source='status_update.id')
    subject_member = member_serializers.Member(source='subject_member')  # noqa # pylint: disable=no-value-for-parameter, unexpected-keyword-arg

    class Meta(object):
        # pylint: disable=too-few-public-methods
        model = models.Newsfeed
        fields = ('id', 'member', 'club_id', 'event_type', 'status_update_id',
                  'subject_member', 'time')
