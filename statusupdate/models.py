from __future__ import unicode_literals

from django.db import models


# TODO - In need of serious love:
#    - The status_id, subject_id, creator_id, club_id, and maybe others, need to be made
#      ForeignKey(s) here and in the DB.
#    - Need to double check many other things
class StatusUpdate(models.Model):
    id = models.IntegerField(primary_key=True)
    status_id = models.IntegerField()
    subject_id = models.IntegerField()
    creator_id = models.IntegerField()
    creator_img = models.CharField(max_length=255)
    has_previewed = models.CharField(db_column='hasPreviewed', max_length=1)
    votes = models.IntegerField()
    updated = models.DateTimeField()
    started = models.DateTimeField()
    is_private = models.CharField(max_length=1)
    expires = models.IntegerField()
    creator_likes = models.IntegerField()
    subject = models.CharField(max_length=255)
    is_verify = models.IntegerField()
    is_explore = models.IntegerField(blank=True, null=True)
    recent_likes = models.TextField()
    club_id = models.IntegerField()
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'tblChallenges'
