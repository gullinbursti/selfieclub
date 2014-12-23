from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from django.db.models import Count


# TODO - Comb through and confirm against DB table!!
class ClubType(models.Model):
    # pylint: disable=too-few-public-methods
    id = models.IntegerField(primary_key=True)
    club_type = models.CharField(unique=True, max_length=16)
    description = models.CharField(max_length=64)
    added = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        managed = False
        db_table = 'tblClubTypeEnum'

    def __unicode__(self):
        """Return unicode representation."""
        return u'{}'.format(self.id)


# TODO - Comb through and confirm against DB table!!
class Club(models.Model):
    # pylint: disable=too-few-public-methods
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    club_type = models.ForeignKey('ClubType')
    owner = models.ForeignKey('member.Member')
    description = models.CharField(max_length=160)
    img = models.CharField(max_length=255)
    lat = models.FloatField(max_length=9)
    lon = models.FloatField(max_length=9)
    coords = {'lat': None, 'lon': None}
    added = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=255)

    class Meta(object):
        managed = False
        db_table = 'club'

    def get_total_members(self):
        # pylint: disable=no-self-use,unused-argument
        # Note that club_member.joined is set to '0000-00-00 00:00:00' if the
        # member has not actually joined the club.  '0000-00-00 00:00:00' is an
        # invalid date and time.  Searching greater then '0001-01-01'.

        count = self.clubmember_set.filter(joined__gte=datetime(1, 1, 1)) \
            .count()
        return count + 1

    def get_total_activity(self):
        # pylint: disable=no-self-use,unused-argument
        status_updates = self.statusupdate_set.count()
        votes = self.statusupdate_set \
            .aggregate(count=Count('statusupdatevoter'))['count']
        return status_updates + votes

    def get_coords(self):
        # pylint: disable=no-self-use,unused-argument
        return {'lat': self.lat, 'lon': self.lon}

    def __unicode__(self):
        """Return unicode representation."""
        return u'{} {}'.format(self.id, self.name)


class ClubLabel(models.Model):
    # pylint: disable=too-few-public-methods
    name = models.CharField(unique=True, max_length=32)
    description = models.CharField(max_length=64)
    club = models.ManyToManyField('Club', related_name='label')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        db_table = 'tbl_club_label'

    def __unicode__(self):
        """Return unicode representation."""
        return u'{}'.format(self.name)
