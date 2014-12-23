from __future__ import absolute_import

from celery import shared_task
from celery.utils.log import get_task_logger
import member
import club
import messaging
import newsfeed_member
import calendar
from club import search

LOGGER = get_task_logger(__name__)


# TODO: Decrypt invitee_phone from the invitee Member object, stop passing it
@shared_task
def invitation_sent(club_id, actor_member_id,
                    invitee_member_id, invitee_phone, when):
    LOGGER.info(
        "Event received: invitation_sent(%s, %s, %s, %s, %s)",
        club_id, actor_member_id, invitee_member_id, invitee_phone, when)

    if not club_exists(club_id):
        LOGGER.debug("Club '%s' does not exist", club_id)
        return

    if not user_exists(actor_member_id):
        LOGGER.debug("Actor '%s' does not exist", actor_member_id)
        return

    receiving_member = member.models.Member.objects.get(pk=invitee_member_id)
    if not receiving_member:
        LOGGER.debug("Invitee '%s' does not exist", invitee_member_id)
        return

    # TODO - Check datetime

    event = newsfeed_member.models.Newsfeed(
        member_id=invitee_member_id,
        club_id=club_id,
        event_type_id=2,  # TODO - CLUB_INVITE_RECEIVED
        time=when
    )
    event.save()

    # Celery's .delay() just means .queue() or .submit() immediately
    if receiving_member.device_token:
        messaging.tasks.send_push_invitation.delay(
            club_id, actor_member_id, invitee_member_id, when)
        LOGGER.info("sending push invitation to %s", invitee_member_id)
    elif invitee_phone:
        messaging.tasks.send_sms_invitation.delay(
            club_id, actor_member_id, invitee_phone, when)
        LOGGER.info("sending SMS invitation to %s", invitee_phone)


@shared_task
def joined(club_id, actor_member_id, when):
    LOGGER.info("Event received: joined(%s, %s, %s)",
                club_id, actor_member_id, when)

    joined_club = club.models.Club.objects.get(pk=club_id)
    if not joined_club:
        LOGGER.debug("Club '%s' does not exist", club_id)
        return

    if not user_exists(actor_member_id):
        LOGGER.debug("Actor '%s' does not exist", actor_member_id)
        return

    # TODO - Check datetime

    # event for joiner
    event = newsfeed_member.models.Newsfeed(
        member_id=actor_member_id,
        subject_member_id=actor_member_id,
        club_id=club_id,
        event_type_id=3,  # TODO - CLUB_JOINED
        time=when
    )
    event.save()
    # event for club owner
    event = newsfeed_member.models.Newsfeed(
        member_id=joined_club.owner.id,
        subject_member_id=actor_member_id,
        club_id=club_id,
        event_type_id=3,  # TODO - CLUB_JOINED
        time=when
    )
    event.save()

    # Celery's .delay() just means .queue() or .submit() immediately
    messaging.tasks.send_push_joined.delay(
        club_id, actor_member_id, joined_club.owner.id)


@shared_task
def index_club(club_id):
    LOGGER.info("Event received: index_club(%s)", club_id)
    club_to_index = club.models.Club.objects.get(pk=club_id)
    if not club_to_index:
        LOGGER.debug("Club '%s' does not exist", club_id)
    params = {'club_id': str(club_to_index.id),
              'type': club_to_index.club_type.club_type,
              'added': calendar.timegm(club_to_index.added.utctimetuple()),
              'lat': club_to_index.lat,
              'lon': club_to_index.lon,
              'owner_id': str(club_to_index.owner.id),
              'username': club_to_index.owner.name,
              'gender': club_to_index.owner.gender,
              'name': club_to_index.name,
              'description': club_to_index.description,
              'tags': club_to_index.tags}
    search.add_club(club_id, params)


@shared_task
def post_status_update(club_id, actor_member_id, selfie_id, when):
    # TODO # pylint: disable=unused-argument
    LOGGER.info("Event received: post_status_update")


def user_exists(user_id):
    return member.models.Member.objects.filter(pk=user_id).exists()


def club_exists(club_id):
    return club.models.Club.objects.filter(pk=club_id).exists()
