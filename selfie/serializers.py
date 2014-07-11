from selfie import models
from rest_framework import serializers


class Selfie(serializers.ModelSerializer):
    class Meta:
        model = models.Selfie
        fields = ('id', 'creator_id', 'is_private', 'votes', 'added')
