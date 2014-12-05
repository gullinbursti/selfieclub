from club import models
from django.forms import widgets
# from django.forms.models import model_to_dict
from rest_framework import serializers
# import json


class ClubType(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    class Meta(object):
        model = models.ClubType
        fields = ('id', 'club_type', 'description', 'added')


class NestedSerializer(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    class Meta(object):
        model = models.Club
        fields = ('lat', 'lon')


class Club(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    coords = NestedSerializer()

    class Meta(object):
        model = models.Club
        fields = ('id', 'name', 'club_type', 'owner', 'description', 'img',
                  'coords', 'lat', 'lon', 'added')


class ClubSummary(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    class Meta(object):
        # pylint: disable=too-few-public-methods
        model = models.Club
        fields = ('id', 'name', 'img', 'owner')


class ClubLabel(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    club_ids = serializers.SlugRelatedField(
        source='club',
        slug_field='id',
        many=True,
        write_only=True,
        widget=widgets.TextInput,
        help_text='Comma delimited array of club_ids.'
    )

    class Meta(object):
        # pylint: disable=too-few-public-methods
        model = models.ClubLabel
        fields = ('id', 'name', 'description', 'club_ids', 'updated',
                  'created')
