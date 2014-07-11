from __future__ import unicode_literals

from django.db import models


# TODO - seriously need to comb through this to make sure it marches
# with MySQL schema
class Member(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    device_token = models.CharField(max_length=64, blank=True)
    fb_id = models.CharField(max_length=255)
    gender = models.CharField(max_length=1)
    img_url = models.CharField(max_length=255)
    bio = models.TextField()
    website = models.CharField(max_length=255)
    paid = models.CharField(max_length=1)
    points = models.IntegerField()
    notifications = models.CharField(max_length=1)
    last_login = models.DateTimeField()
    age = models.IntegerField()
    adid = models.CharField(unique=True, max_length=36, blank=True)
    abuse_ct = models.IntegerField()
    total_challenges = models.IntegerField()
    total_votes = models.IntegerField()
    sms_verified = models.IntegerField()
    email = models.CharField(unique=True, max_length=100, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'tblUsers'
