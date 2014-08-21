from __future__ import absolute_import
from urllib import quote_plus
from celery import shared_task
from celery.utils.log import get_task_logger
from .nexmo import send_sms_message
from .amazon import send_push_message
import club
import member
import re


logger = get_task_logger(__name__)


@shared_task
def send_sms_invitation(club_id, actor_member_id, invitee_sms_number, when):
    logger.info("Event received: send_sms_invitation({}, {}, {}, {})"
                .format(club_id, actor_member_id, invitee_sms_number, when))

    to = validate_sms_number(invitee_sms_number)
    if not to:
        logger.debug("SMS target '{}' is invalid".format(invitee_sms_number))
        return

    clubToJoin = club.models.Club.objects.get(pk=club_id)
    if not clubToJoin:
        logger.debug("Club '{}' does not exist".format(club_id))
        return

    sendingMember = member.models.Member.objects.get(pk=actor_member_id)
    if not sendingMember:
        logger.debug("Actor '{}' does not exist".format(actor_member_id))
        return

    # TODO - Check datetime

    clubNameForUrl = quote_plus(clubToJoin.name)
    message = '{0} has invited you to {1}! http://joinselfie.club/{0}/{2} ' \
        .format(sendingMember.name, clubToJoin.name, clubNameForUrl) + \
        'Reply YES to receive updates'
    result = send_sms_message(to, message)
    logger.info("Event handled: send_sms_message({}, {}) {}" .format(
        to, message, result))


@shared_task
def send_push_invitation(club_id, actor_member_id, invitee_member_id, when):
    logger.info("Event received: send_push_invitation({}, {}, {}, {})"
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
    to = 'arn:aws:sns:us-east-1:892810128873:Selfieclub_SMS_Dev'
    message = '{} has invited you to join {}!'.format(
        sendingMember.name, clubToJoin.name)
    result = send_push_message(to, message)
    logger.info("Event handled: send_push_message({}, {}) = {}".format(
        to, message, result))


def validate_sms_number(sms_number):
    """Expects numeric, with an optional leading + symbol, which it returns"""
    match = re.match("^(\+?)(\d+)$", sms_number)
    if match:
        return '+' + match.group(2)
    return False
