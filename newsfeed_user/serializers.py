from newsfeed_user import models
from rest_framework import serializers


class NewsfeedType(serializers.ModelSerializer):
    class Meta:
        model = models.NewsfeedType
        fields = ('id', 'name', 'description', 'updated', 'created')


class NewsfeedEvent(serializers.ModelSerializer):
    event_type_id = serializers.SlugRelatedField(slug_field='name', read_only=False)

    class Meta:
        model = models.NewsfeedEvent
        fields = ('id', 'user_id', 'club_id', 'event_type_id', 'selfie_id', 'time', 'updated', 'created')
