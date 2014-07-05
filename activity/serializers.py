from rest_framework import serializers
from activity import models


class Activity(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = ('id', 'activity_type', 'selfie_id', 'user_id', 'club_id', 'time')
