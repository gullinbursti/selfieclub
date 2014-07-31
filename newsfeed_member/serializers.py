from newsfeed_member import models
from rest_framework import serializers
from member import serializers as member_serializers


class NewsfeedType(serializers.ModelSerializer):
    class Meta:
        model = models.NewsfeedType
        fields = ('id', 'name', 'description', 'updated', 'created')


class Newsfeed(serializers.ModelSerializer):
    event_type = serializers.SlugRelatedField(source='event_type', slug_field='name', read_only=False)
    member = member_serializers.Member(source='member')

    class Meta:
        model = models.Newsfeed
        fields = ('id', 'member', 'club', 'event_type', 'status_update_id', 'time')
