from __future__ import unicode_literals

from django.db import models


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
    added = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        managed = False
        db_table = 'club'

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
