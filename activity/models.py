from django.db import models


ACTIVITY_TYPES = (
    (1, 'VERIFIED'),              # 1 - VERIFIED (LIKES/UPVOTES HAS SURPASSED THRESHOLD)
    (3, 'RECEIVED_UPVOTE'),       # 3 - RECEIVED AN UPVOTE / LIKE ON A PHOTO SUBMISSION
    (5, 'RECEIVED_REPLY'),        # 5 - RECEIVED A PHOTO REPLY TO A PHOTO SUBMISSION
    (6, 'CLUB_JOIN'),             # 6 - CLUB INVITE WAS ACCEPTED
    (7, 'CLUB_QUIT'),             # 7 - SOMEONE QUIT A CLUB OWNED BY THE THIS USER
    (8, 'CLUB_INVITATION'),       # 8 - RECEIVED A CLUB INVITATION
    (9, 'CLUB_PHOTO_SUBMITION'),  # 9 - A PHOTO WAS SUBMITTED TO A CLUB THIS USER OWNS
    (10, 'CLUB_REPLY'),           # 10 - A PHOTO/REPLY WAS SUBMITTED TO A CLUB
)


class Activity(models.Model):
    activity_type = models.PositiveSmallIntegerField(choices=ACTIVITY_TYPES, max_length=3)
    post_id = models.IntegerField(max_length=10, db_index=True)
    # TODO: more
    user_id = models.IntegerField(max_length=10, db_index=True)
    club_id = models.IntegerField(max_length=11, db_index=True)
    club_name = models.CharField(max_length=255)
    time = models.DateTimeField()

    class Meta:
        ordering = ['-time']
        db_table = 'tbl_activity'
