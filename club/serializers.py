from club import models
from rest_framework import serializers


class ClubType(serializers.ModelSerializer):
    class Meta:
        model = models.ClubType
        fields = ('id', 'club_type', 'description', 'added')
