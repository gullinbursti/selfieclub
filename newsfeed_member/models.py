from django.db import models


class NewsfeedType(models.Model):
    # TODO # pylint: disable=model-missing-unicode
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_newsfeed_member_event_type'

    def __unicode__(self):
        """Return unicode representation."""
        return u'{}'.format(self.name)


# TODO - ForeignKey on club_id not created in DB
class Newsfeed(models.Model):
    # TODO # pylint: disable=model-missing-unicode
    member = models.ForeignKey('member.Member')
    club = models.ForeignKey('club.Club')
    event_type = models.ForeignKey('NewsfeedType')
    status_update = models.ForeignKey('status.StatusUpdate', null=True)
    subject_member = models.ForeignKey(
        'member.Member',
        related_name='subject_member',
        null=True)
    time = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time']
        db_table = 'tbl_newsfeed_member_event'

    def __unicode__(self):
        """Return unicode representation."""
        return u'{}'.format(self.time)
