from club import models
from django.forms import widgets
from drf_compound_fields.fields import DictField
from rest_framework import serializers
import member


class ClubType(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    class Meta(object):
        model = models.ClubType
        fields = ('id', 'club_type', 'description', 'added')


class Club(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    coords = DictField(read_only=True, source='get_coords')
    total_members = serializers.IntegerField(read_only=True,
                                             source='get_total_members')
    total_activity = serializers.IntegerField(read_only=True,
                                              source='get_total_activity')
    # TODO - Depricate 'owner' in favor of 'owner_member'.
    owner_member = member.serializers.MemberSummary(read_only=True,
                                                    source='owner')

    class Meta(object):
        model = models.Club
        fields = ('id', 'name', 'club_type', 'owner', 'owner_member',
                  'description', 'img', 'total_members', 'total_activity',
                  'coords', 'added')


class ClubSearch(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    coords = DictField(read_only=True, source='get_coords')

    class Meta(object):
        # pylint: disable=too-few-public-methods
        model = models.Club
        fields = ('id', 'name', 'coords', 'added', 'tags')


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
