from __future__ import unicode_literals

from django.db import models


# TODO - Cumb through and confirm against DB table!!
class ClubType(models.Model):
    id = models.IntegerField(primary_key=True)
    club_type = models.CharField(unique=True, max_length=16)
    description = models.CharField(max_length=64)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'tblClubTypeEnum'

# class Club(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(unique=True, max_length=255)
#     club_type = models.ForeignKey('Tblclubtypeenum')
#     added = models.DateTimeField()
#     owner = models.ForeignKey('Tblusers')
#     description = models.CharField(max_length=160)
#     img = models.CharField(max_length=255)
#
#     class Meta:
#         managed = False
#         db_table = 'club'
