from django.db import models


class NewsfeedType(models.Model):
    name = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=64)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_newsfeed_user_event_type'


class NewsfeedEvent(models.Model):
    user_id = models.ForeignKey('member.Member', db_column='user_id')
    club_id = models.ForeignKey('club.Club', db_column='club_id')
    event_type_id = models.ForeignKey('NewsfeedType', db_column='event_type_id')
    selfie_id = models.IntegerField(max_length=10)
    time = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time']
        db_table = 'tbl_newsfeed_user_event'
