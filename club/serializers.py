from club import models
from django.forms import widgets
from rest_framework import serializers


class ClubType(serializers.ModelSerializer):
    class Meta:
        model = models.ClubType
        fields = ('id', 'club_type', 'description', 'added')


class Club(serializers.ModelSerializer):
    class Meta:
        model = models.Club
        fields = ('id', 'name', 'club_type', 'owner', 'description', 'img', 'added')


class ClubSummary(serializers.ModelSerializer):
    class Meta:
        model = models.Club
        fields = ('id', 'name')


class ClubLabel(serializers.ModelSerializer):
    clubs = ClubSummary(
        many=True,
        source='club',
        read_only=True
    )
    club_ids = serializers.SlugRelatedField(
        source='club',
        slug_field='id',
        many=True,
        write_only=True,
        widget=widgets.TextInput, help_text='Comma delimited array of club_ids.'
    )

    class Meta:
        model = models.ClubLabel
        fields = ('id', 'name', 'description', 'clubs', 'club_ids', 'updated', 'created')
