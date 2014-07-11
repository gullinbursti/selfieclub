from django.db import models


class NewsfeedType(models.Model):
    name = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=64)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_newsfeed_user_event_type'


class NewsfeedEvent(models.Model):
    user = models.ForeignKey('member.Member')
    club = models.ForeignKey('club.Club')
    event_type = models.ForeignKey('NewsfeedType')
    selfie_id = models.IntegerField(max_length=10)
    time = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time']
        db_table = 'tbl_newsfeed_user_event'
