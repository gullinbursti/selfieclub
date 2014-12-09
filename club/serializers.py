from club import models
from datetime import datetime
from django.forms import widgets
from member import models as member_models
from status import models as status_models
from rest_framework import serializers


class ClubType(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    class Meta(object):
        model = models.ClubType
        fields = ('id', 'club_type', 'description', 'added')


class GeoCoordinateSerializer(serializers.Serializer):
    # pylint: disable=too-few-public-methods
    lat = serializers.FloatField
    lon = serializers.FloatField


class Club(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    coords = GeoCoordinateSerializer(read_only=True, source='*')
    total_members = serializers.IntegerField(read_only=True, source='*')
    total_status_updates = serializers.IntegerField(read_only=True, source='*')

    def transform_total_members(self, obj, value):
        # pylint: disable=no-self-use,unused-argument
        # Note that club_member.joined is set to '0000-00-00 00:00:00' if the
        # member has not actually joined the club.  '0000-00-00 00:00:00' is an
        # invalid date and time.  Searching greater then '0001-01-01'.
        count = member_models.ClubMember.objects.filter(club=obj.id) \
            .filter(joined__gte=datetime(1, 1, 1)).count()
        # +1 to include the owner
        return count + 1

    def transform_total_status_updates(self, obj, value):
        # pylint: disable=no-self-use,unused-argument
        count = status_models.StatusUpdate.objects.filter(club=obj.id).count()
        return count

    def transform_coords(self, obj, value):
        # pylint: disable=no-self-use,unused-argument
        return {'lat': obj.lat, 'lon': obj.lon}

    class Meta(object):
        model = models.Club
        fields = ('id', 'name', 'club_type', 'owner', 'description', 'img',
                  'total_members', 'total_status_updates', 'coords', 'added')


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
