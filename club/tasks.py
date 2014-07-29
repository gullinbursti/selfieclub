from __future__ import absolute_import

from celery import shared_task
import member
import logging

logger = logging.getLogger(__name__)


@shared_task
def invitation_sent(club_id, actor_member_id, invitee_member_id, when):
    logger.info("Event received: invitation_sent({}, {}, {}, {})"
                .format(club_id, actor_member_id, invitee_member_id, when))

    if not user_exists(actor_member_id):
        logger.debug("Actor '{}' does not exist".format(actor_member_id))
        return

    if not user_exists(invitee_member_id):
        logger.debug("Invitee '{}' does not exist".format(invitee_member_id))
        return


@shared_task
def joined(club_id, actor_member_id, when):
    logger.info("Event received: joined")
    pass


@shared_task
def quit(club_id, actor_member_id, when):
    logger.info("Event received: quit")
    pass


@shared_task
def post_status_update(club_id, actor_member_id, selfie_id, when):
    logger.info("Event received: post_status_update")
    pass


def user_exists(pk):
    member.models.Member.objects.filter(pk=pk).exists()
