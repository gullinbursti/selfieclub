# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class BootConf(models.Model):
    data = models.TextField(blank=True)
    type = models.CharField(primary_key=True, max_length=36)
    last_update = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'boot_conf'

# Moved to /club/
# ----
# class Club(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(unique=True, max_length=255)
#     club_type = models.ForeignKey('Tblclubtypeenum')
#     added = models.DateTimeField()
#     owner = models.ForeignKey('Tblusers')
#     description = models.CharField(max_length=160)
#     img = models.CharField(max_length=255)
#     class Meta:
#         managed = False
#         db_table = 'club'

class ClubMember(models.Model):
    club = models.ForeignKey(Club)
    extern_name = models.CharField(max_length=255, blank=True)
    mobile_number = models.CharField(max_length=25, blank=True)
    email = models.CharField(max_length=255, blank=True)
    pending = models.IntegerField(blank=True, null=True)
    blocked = models.IntegerField()
    user = models.ForeignKey('Tblusers', blank=True, null=True)
    invited = models.DateTimeField()
    joined = models.DateTimeField()
    blocked_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'club_member'

class ExploreIds(models.Model):
    id = models.IntegerField(primary_key=True)
    updated = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'explore_ids'

class InviteMessages(models.Model):
    type = models.CharField(primary_key=True, max_length=36)
    message = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'invite_messages'

class MobileNumbers(models.Model):
    user_id = models.IntegerField()
    number = models.CharField(max_length=15)
    class Meta:
        managed = False
        db_table = 'mobile_numbers'

class Persona(models.Model):
    network = models.CharField(max_length=36)
    email = models.CharField(max_length=256)
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=255)
    extra = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'persona'

class Tblchallengeparticipantsubjectmap(models.Model):
    challenge_participant_id = models.IntegerField()
    subject_id = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'tblChallengeParticipantSubjectMap'

class Tblchallengeparticipants(models.Model):
    id = models.IntegerField(primary_key=True)
    challenge = models.ForeignKey('Tblchallenges')
    user = models.ForeignKey('Tblusers')
    img = models.CharField(max_length=255, blank=True)
    joined = models.IntegerField()
    likes = models.IntegerField()
    subject = models.CharField(max_length=255, blank=True)
    has_viewed = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'tblChallengeParticipants'

class Tblchallengestatustypes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    info = models.CharField(max_length=255)
    added = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'tblChallengeStatusTypes'

class Tblchallengesubjectmap(models.Model):
    challenge_id = models.IntegerField()
    subject_id = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'tblChallengeSubjectMap'

class Tblchallengesubjects(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    creator_id = models.IntegerField()
    itunes_id = models.CharField(max_length=255)
    linkshare_url = models.CharField(max_length=255)
    added = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'tblChallengeSubjects'

class Tblchallengevotes(models.Model):
    id = models.IntegerField(primary_key=True)
    challenge_id = models.IntegerField()
    user = models.ForeignKey('Tblusers')
    challenger_id = models.IntegerField()
    added = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'tblChallengeVotes'

# Moved to /selfie/
# class Tblchallenges(models.Model):
#     id = models.IntegerField(primary_key=True)
#     status_id = models.IntegerField()
#     subject_id = models.IntegerField()
#     creator_id = models.IntegerField()
#     creator_img = models.CharField(max_length=255)
#     haspreviewed = models.CharField(db_column='hasPreviewed', max_length=1) # Field name made lowercase.
#     votes = models.IntegerField()
#     updated = models.DateTimeField()
#     started = models.DateTimeField()
#     added = models.DateTimeField()
#     is_private = models.CharField(max_length=1)
#     expires = models.IntegerField()
#     creator_likes = models.IntegerField()
#     subject = models.CharField(max_length=255)
#     is_verify = models.IntegerField()
#     is_explore = models.IntegerField(blank=True, null=True)
#     recent_likes = models.TextField()
#     club_id = models.IntegerField()
#     class Meta:
#         managed = False
#         db_table = 'tblChallenges'

# Moved to /club/
# ----
# class Tblclubtypeenum(models.Model):
#     id = models.IntegerField(primary_key=True)
#     club_type = models.CharField(unique=True, max_length=16)
#     description = models.CharField(max_length=64)
#     added = models.DateTimeField()
#     class Meta:
#         managed = False
#         db_table = 'tblClubTypeEnum'

class Tblcommentstatustypes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    info = models.CharField(max_length=255)
    added = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'tblCommentStatusTypes'

class Tblcomments(models.Model):
    id = models.IntegerField(primary_key=True)
    challenge_id = models.IntegerField()
    user_id = models.IntegerField()
    text = models.CharField(max_length=255)
    status_id = models.IntegerField()
    added = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'tblComments'

class Tblflaggedchallenges(models.Model):
    challenge_id = models.IntegerField()
    user_id = models.IntegerField()
    added = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'tblFlaggedChallenges'

class Tblflaggeduserapprovals(models.Model):
    challenge = models.ForeignKey(Tblchallenges)
    user = models.ForeignKey('Tblusers')
    flag = models.IntegerField()
    added = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'tblFlaggedUserApprovals'

class Tblinvitedusers(models.Model):
    id = models.IntegerField(primary_key=True)
    fb_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    added = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'tblInvitedUsers'

class Tblshoutouts(models.Model):
    challenge_id = models.IntegerField()
    target_challenge_id = models.IntegerField()
    target_user_id = models.IntegerField()
    added = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'tblShoutouts'

class Tbluserphones(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('Tblusers')
    phone_number_enc = models.CharField(unique=True, max_length=64)
    verified = models.IntegerField(blank=True, null=True)
    verified_date = models.DateTimeField(blank=True, null=True)
    verify_code = models.CharField(max_length=10, blank=True)
    verify_count_down = models.IntegerField(blank=True, null=True)
    verify_count_total = models.IntegerField(blank=True, null=True)
    verify_last_attempt = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'tblUserPhones'

class Tbluserpokes(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    poker_id = models.IntegerField()
    added = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'tblUserPokes'

# moved to /member/
# ----
# class Tblusers(models.Model):
#     id = models.IntegerField(primary_key=True)
#     username = models.CharField(unique=True, max_length=255)
#     device_token = models.CharField(max_length=64, blank=True)
#     fb_id = models.CharField(max_length=255)
#     gender = models.CharField(max_length=1)
#     img_url = models.CharField(max_length=255)
#     bio = models.TextField()
#     website = models.CharField(max_length=255)
#     paid = models.CharField(max_length=1)
#     points = models.IntegerField()
#     notifications = models.CharField(max_length=1)
#     last_login = models.DateTimeField()
#     added = models.DateTimeField()
#     age = models.IntegerField()
#     adid = models.CharField(unique=True, max_length=36, blank=True)
#     abuse_ct = models.IntegerField()
#     total_challenges = models.IntegerField()
#     total_votes = models.IntegerField()
#     sms_verified = models.IntegerField()
#     email = models.CharField(unique=True, max_length=100, blank=True)
#     class Meta:
#         managed = False
#         db_table = 'tblUsers'

class TumblrSelfies(models.Model):
    id = models.BigIntegerField(unique=True)
    data = models.TextField()
    time = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'tumblr_selfies'

class UserArchive(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    data = models.TextField(blank=True)
    added = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'user_archive'

