from newsfeed_member import models
from rest_framework import serializers
from member import serializers as member_serializers


class NewsfeedType(serializers.ModelSerializer):
    class Meta:
        model = models.NewsfeedType
        fields = ('id', 'name', 'description', 'updated', 'created')


class Newsfeed(serializers.ModelSerializer):
    event_type = serializers.SlugRelatedField(source='event_type_id', slug_field='name', read_only=False)
    member = member_serializers.Member(source='member_id')

    class Meta:
        model = models.Newsfeed
        fields = ('id', 'member', 'club_id', 'event_type', 'selfie_id', 'time')
