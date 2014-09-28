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
        fields = ('id', 'name', 'club_type', 'owner', 'description', 'img',
                  'added')


class ClubSummary(serializers.ModelSerializer):
    class Meta:
        model = models.Club
        fields = ('id', 'name', 'img', 'owner')


class ClubLabel(serializers.ModelSerializer):
    club_ids = serializers.SlugRelatedField(
        source='club',
        slug_field='id',
        many=True,
        write_only=True,
        widget=widgets.TextInput,
        help_text='Comma delimited array of club_ids.'
    )

    class Meta:
        model = models.ClubLabel
        fields = ('id', 'name', 'description', 'club_ids', 'updated',
                  'created')
