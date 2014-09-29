from django.test import TestCase
from newsfeed_member.models import Newsfeed, NewsfeedType


class NewsfeedTestCase(TestCase):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-public-methods
    def setUp(self):
        NewsfeedType.objects.create(id=1, name='CLUB_INVITE_RECEIVED')
        NewsfeedType.objects.create(id=2, name='CLUB_JOINED')
        Newsfeed.objects.create(
            club_id=122,
            event_type_id=1,
            member_id=14866,
            status_update_id=None,
            time='2014-08-14T19:42:22Z')
        Newsfeed.objects.create(
            club_id=122,
            event_type_id=2,
            member_id=2466,
            status_update_id=None,
            time='2014-08-14T19:42:30Z')

    def test_event_type_foreign_keys_are_valid(self):
        """Newsfeed event type IDs link to other objects."""
        invite_item = Newsfeed.objects.get(member_id=14866)
        self.assertEqual(invite_item.event_type.name, 'CLUB_INVITE_RECEIVED')
        invite_item = Newsfeed.objects.get(member_id=2466)
        self.assertEqual(invite_item.event_type.name, 'CLUB_JOINED')
