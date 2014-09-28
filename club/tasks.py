from __future__ import absolute_import

from celery import shared_task
from celery.utils.log import get_task_logger
import member
import club
import messaging
import newsfeed_member


logger = get_task_logger(__name__)


# TODO: Decrypt invitee_phone from the invitee Member object, stop passing it
@shared_task
def invitation_sent(club_id, actor_member_id,
                    invitee_member_id, invitee_phone, when):
    logger.info(
        "Event received: invitation_sent(%s, %s, %s, %s, %s)",
        club_id, actor_member_id, invitee_member_id, invitee_phone, when)

    if not club_exists(club_id):
        logger.debug("Club '%s' does not exist", club_id)
        return

    if not user_exists(actor_member_id):
        logger.debug("Actor '%s' does not exist", actor_member_id)
        return

    receivingMember = member.models.Member.objects.get(pk=invitee_member_id)
    if not receivingMember:
        logger.debug("Invitee '%s' does not exist", invitee_member_id)
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
    if receivingMember.device_token:
        messaging.tasks.send_push_invitation.delay(
            club_id, actor_member_id, invitee_member_id, when)
        logger.info("sending push invitation to %s", invitee_member_id)
    elif invitee_phone:
        messaging.tasks.send_sms_invitation.delay(
            club_id, actor_member_id, invitee_phone, when)
        logger.info("sending SMS invitation to %s", invitee_phone)


@shared_task
def joined(club_id, actor_member_id, when):
    logger.info("Event received: joined(%s, %s, %s)",
                club_id, actor_member_id, when)

    joined_club = club.models.Club.objects.get(pk=club_id)
    if not joined_club:
        logger.debug("Club '%s' does not exist", club_id)
        return

    if not user_exists(actor_member_id):
        logger.debug("Actor '%s' does not exist", actor_member_id)
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
        joined_club.name, joined_club.owner.id, actor_member_id)


@shared_task
def quit(club_id, actor_member_id, when):
    logger.info("Event received: quit")
    pass


@shared_task
def post_status_update(club_id, actor_member_id, selfie_id, when):
    logger.info("Event received: post_status_update")
    pass


def user_exists(pk):
    return member.models.Member.objects.filter(pk=pk).exists()


def club_exists(pk):
    return club.models.Club.objects.filter(pk=pk).exists()
