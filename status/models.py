from __future__ import unicode_literals

from django.db import models
import json


# TODO - In need of serious love:
#    - The status_id, subject_id, creator_id, club_id, and maybe others, need
#      to be made
#      ForeignKey(s) here and in the DB.
#    - Need to double check many other things
class StatusUpdate(models.Model):
    # pylint: disable=too-few-public-methods
    id = models.IntegerField(primary_key=True)
    parent = models.ForeignKey('self')
    status_id = models.IntegerField()
    subject_id = models.IntegerField()
    creator = models.ForeignKey('member.Member')
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
    club = models.ForeignKey('club.Club')
    added = models.DateTimeField(auto_now_add=True)
    # DEPRREICATED - `subjects` no longer in use, see `Emotion`.
    subjects = models.ManyToManyField(
        'StatusUpdateSubject', through='StatusUpdateSubjectMap',
        through_fields=('status_update', 'status_update_subject'))

    class Meta:
        managed = False
        db_table = 'tblChallenges'

    def get_emotions(self):
        emotions_json = self.statusupdateemotion.emotion_id_json  # NOQA - pylint: disable=no-member
        result = []
        if emotions_json:
            emotion_ids = json.loads(emotions_json)
            # TODO: look into caching this in memory somewhere
            emotions_map = dict(
                Emotion.objects.filter(id__in=list(set(emotion_ids)))
                .values_list('id', 'title'))
            result = [emotions_map[long(x)]
                      for x in emotion_ids if long(x) in emotions_map]
        return result

    def __unicode__(self):
        """Return unicode representation."""
        return u'{}'.format(self.id)


class Emotion(models.Model):
    # pylint: disable=too-few-public-methods
    id = models.IntegerField(primary_key=True)
    title = models.CharField(unique=True, max_length=32)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_emotion'

    def __unicode__(self):
        """Return unicode representation."""
        return u'{}'.format(self.id)


class StatusUpdateEmotion(models.Model):
    # pylint: disable=too-few-public-methods
    status_update = models.OneToOneField(StatusUpdate, primary_key=True)
    emotion_id_count = models.IntegerField()
    emotion_id_json = models.TextField()

    class Meta:
        managed = False
        db_table = 'tbl_status_update_emotion'

    def __unicode__(self):
        """Return unicode representation."""
        return u'{}'.format(self.status_update)


class StatusUpdateViewer(models.Model):
    # pylint: disable=too-few-public-methods
    id = models.IntegerField(primary_key=True)
    member = models.ForeignKey('member.Member')
    status_update = models.ForeignKey('StatusUpdate')
    viewed_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'tbl_status_update_viewer'

    def __unicode__(self):
        """Return unicode representation."""
        return u'{} {}'.format(self.member, self.status_update)


class StatusUpdateVoter(models.Model):
    # pylint: disable=too-few-public-methods
    id = models.IntegerField(primary_key=True)
    member = models.ForeignKey('member.Member')
    status_update = models.ForeignKey('StatusUpdate')
    vote = models.IntegerField()
    voted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'tbl_status_update_voter'

    def __unicode__(self):
        """Return unicode representation."""
        return u'{} {} {}'.format(self.member, self.vote, self.status_update)


class StatusUpdateSubject(models.Model):

    """
    DEPRREICATED - `StatusUpdateSubject` is no longer in use.

    Use `Emotion` instead.
    """

    # pylint: disable=too-few-public-methods
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    creator_member_id = models.IntegerField(db_column='creator_id')
    itunes_id = models.CharField(max_length=255)
    linkshare_url = models.CharField(max_length=255)
    added = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tblChallengeSubjects'

    def __unicode__(self):
        """Return unicode representation."""
        return u'{}'.format(self.id)


class StatusUpdateSubjectMap(models.Model):
    # pylint: disable=too-few-public-methods
    status_update = models.ForeignKey('StatusUpdate', db_column='challenge_id')
    status_update_subject = models.ForeignKey('StatusUpdateSubject',
                                              db_column='subject_id')

    """
    DEPRREICATED - `StatusUpdateSubjectMap` is no longer in use.

    Use `StatusUpdateEmotion` instead.
    """

    class Meta:
        managed = False
        db_table = 'tblChallengeSubjectMap'

    def __unicode__(self):
        """Return unicode representation."""
        return u'{}, {}'.format(
            self.status_update, self.status_update_subject)
