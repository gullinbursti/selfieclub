from django.db import models


class NewsfeedType(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_newsfeed_member_event_type'


# TODO - ForeignKey on club_id not created in DB
class Newsfeed(models.Model):
    member_id = models.ForeignKey('member.Member', db_column='member_id')
    club_id = models.ForeignKey('club.Club', db_column='club_id')
    event_type_id = models.ForeignKey('NewsfeedType', db_column='event_type_id')
    status_update_id = models.IntegerField(max_length=10)
    time = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time']
        db_table = 'tbl_newsfeed_member_event'
