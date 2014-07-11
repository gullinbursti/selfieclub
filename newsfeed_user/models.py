from django.db import models

ACTIVITY_TYPES = (
    (0, 'ALL'),                   # 0 - All
    (1, 'VERIFIED'),              # 1 - VERIFIED (LIKES/UPVOTES HAS SURPASSED THRESHOLD)
    (3, 'RECEIVED_UPVOTE'),       # 3 - RECEIVED AN UPVOTE / LIKE ON A PHOTO SUBMISSION
    (5, 'RECEIVED_REPLY'),        # 5 - RECEIVED A PHOTO REPLY TO A PHOTO SUBMISSION
    (6, 'CLUB_JOIN'),             # 6 - CLUB INVITE WAS ACCEPTED
    (7, 'CLUB_QUIT'),             # 7 - SOMEONE QUIT A CLUB OWNED BY THE THIS USER
    (8, 'CLUB_INVITATION'),       # 8 - RECEIVED A CLUB INVITATION
    (9, 'CLUB_PHOTO_SUBMITION'),  # 9 - A PHOTO WAS SUBMITTED TO A CLUB THIS USER OWNS
    (10, 'CLUB_REPLY'),           # 10 - A PHOTO/REPLY WAS SUBMITTED TO A CLUB
)


class NewsfeedType(models.Model):
    name = models.CharField(max_length=16)
    description = models.CharField(max_length=64)
    created = models.DateTimeField()

    class Meta:
        db_table = 'tbl_newsfeed_user_entry_type'
