from statusupdate import models
from rest_framework import serializers


class StatusUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.StatusUpdate
        fields = ('id', 'creator_id', 'is_private', 'votes', 'added')
