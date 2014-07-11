from newsfeed_user import models
from rest_framework import serializers
from member import serializers as member_serializers


class NewsfeedType(serializers.ModelSerializer):
    class Meta:
        model = models.NewsfeedType
        fields = ('id', 'name', 'description', 'updated', 'created')


class NewsfeedEvent(serializers.ModelSerializer):
    event_type = serializers.SlugRelatedField(source='event_type_id', slug_field='name', read_only=False)
    user = member_serializers.Member(source='user_id')

    class Meta:
        model = models.NewsfeedEvent
        fields = ('id', 'user', 'club_id', 'event_type', 'selfie_id', 'time')
