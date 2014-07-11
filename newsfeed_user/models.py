from django.db import models


class NewsfeedType(models.Model):
    name = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=64)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_newsfeed_user_event_type'


class NewsfeedEvent(models.Model):
    user_id = models.IntegerField(max_length=10, db_index=True)
    club_id = models.IntegerField(max_length=11, db_index=True)
    event_type_id = models.ForeignKey(NewsfeedType)
    selfie_id = models.IntegerField(max_length=10)
    time = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time']
        db_table = 'tbl_newsfeed_user_event'
