from __future__ import absolute_import
from urllib import quote_plus
from celery import shared_task
from celery.utils.log import get_task_logger
from .utils import send_sms_message
import club
import member


logger = get_task_logger(__name__)


@shared_task
def send_sms_invitation(club_id, actor_member_id, invitee_member_id, when):
    logger.info("Event received: send_sms_invitation({}, {}, {}, {})"
                .format(club_id, actor_member_id, invitee_member_id, when))

    clubToJoin = club.models.Club.objects.get(pk=club_id)
    if not clubToJoin:
        logger.debug("Club '{}' does not exist".format(club_id))
        return

    sendingMember = member.models.Member.objects.get(pk=actor_member_id)
    if not sendingMember:
        logger.debug("Actor '{}' does not exist".format(actor_member_id))
        return

    receivingMember = member.models.Member.objects.get(pk=invitee_member_id)
    if not receivingMember:
        logger.debug("Invitee '{}' does not exist".format(invitee_member_id))
        return

    # TODO - Check datetime

    clubNameForUrl = quote_plus(clubToJoin.name)
    # TODO: Get SMS number from invitee_member_id
    to = '+12144029466'
    message = "{0} has invited you to {1}! http://joinselfie.club/{0}/{2} Reply YES to receive updates".format(sendingMember.name, clubToJoin.name, clubNameForUrl)
    send_sms_message(to, message)
    logger.info("Event handled: send_sms_message({}, {})" .format(to, message))
