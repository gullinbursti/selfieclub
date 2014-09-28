from __future__ import absolute_import

from celery import shared_task
from celery.utils.log import get_task_logger
import member
import club
import messaging
import newsfeed_member


logger = get_task_logger(__name__)


@shared_task
def post_status_update(club_id, actor_member_id, invitee_member_id, when):
    logger.info("Event received: invitation_sent(%s, %s, %s, %s)",
                club_id, actor_member_id, invitee_member_id, when)

    if not club_exists(club_id):
        logger.debug("Club '%s' does not exist", (club_id))
        return

    if not user_exists(actor_member_id):
        logger.debug("Actor '%s' does not exist", (actor_member_id))
        return

    receivingMember = member.models.Member.objects.get(pk=invitee_member_id)
    if not receivingMember:
        logger.debug("Invitee '%s' does not exist", (invitee_member_id))
        return

    # TODO - Check datetime

    event = newsfeed_member.models.Newsfeed(
        member_id=invitee_member_id,
        subject_member_id=actor_member_id,
        club_id=club_id,
        event_type_id=4,  # TODO - STATUS_UPDATE_CREATED
        time=when
    )
    event.save()

    # Celery's .delay() just means .queue() or .submit() immediately
    if receivingMember.device_token:
        messaging.tasks.send_push_status_update.delay(
            club_id, actor_member_id, invitee_member_id, when)
        logger.info("sending push notification to %s", invitee_member_id)


def user_exists(pk):
    return member.models.Member.objects.filter(pk=pk).exists()


def club_exists(pk):
    return club.models.Club.objects.filter(pk=pk).exists()