from newsfeed_member import models
from rest_framework import serializers
from member import serializers as member_serializers


class NewsfeedType(serializers.ModelSerializer):
    class Meta:
        model = models.NewsfeedType
        fields = ('id', 'name', 'description', 'updated', 'created')


class Newsfeed(serializers.ModelSerializer):
    event_type = serializers.SlugRelatedField(
        source='event_type',
        slug_field='name',
        read_only=False)
    member = member_serializers.Member(source='member')
    club_id = serializers.Field(source='club.id')
    status_update_id = serializers.Field(source='status_update.id')
    subject_member = member_serializers.Member(source='subject_member')

    class Meta:
        model = models.Newsfeed
        fields = ('id', 'member', 'club_id', 'event_type', 'status_update_id',
                  'subject_member', 'time')
