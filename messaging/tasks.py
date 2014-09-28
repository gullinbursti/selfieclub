from __future__ import absolute_import
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from string import Template
from urllib import quote_plus
from .nexmo import send_sms_message, send_unicode_message
from .amazon import send_push_message
import club
import member
import re


logger = get_task_logger(__name__)


@shared_task
def send_sms_invitation(club_id, actor_member_id, invitee_sms_number, when):
    logger.info("Event received: send_sms_invitation(%s, %s, %s, %s)",
                (club_id, actor_member_id, invitee_sms_number, when))

    to = validate_sms_number(invitee_sms_number)
    if not to:
        logger.debug("SMS target '%s' is invalid", (invitee_sms_number))
        return

    clubToJoin = club.models.Club.objects.get(pk=club_id)
    if not clubToJoin:
        logger.debug("Club '%s' does not exist", (club_id))
        return

    sendingMember = member.models.Member.objects.get(pk=actor_member_id)
    if not sendingMember:
        logger.debug("Actor '%s' does not exist", (actor_member_id))
        return

    # TODO - Check datetime

    # TODO: Localize
    template = Template(settings.SMS_INVITE_TEXT)
    message = template.substitute(senderName=sendingMember.name,
                                  clubName=clubToJoin.name,
                                  clubUrlName=quote_plus(clubToJoin.name))
    result = send_sms_message(to, message)
    logger.info("Event handled: send_sms_invitation(%s, %s) %s",
                (to, message, result))


@shared_task
def send_sms_thanks(thankee_sms_number):
    logger.info("Event received: send_sms_thanks(%s)", (thankee_sms_number))

    to = validate_sms_number(thankee_sms_number)
    if not to:
        logger.debug("SMS target '%s' is invalid", (thankee_sms_number))
        return

    message = settings.SMS_THANKS_TEXT
    result = send_sms_message(to, message)
    logger.info("Event handled: sms_thanks(%s, %s) %s",
                (to, message, result))


@shared_task
def send_push_invitation(club_id, actor_member_id, invitee_member_id, when):
    logger.info("Event received: send_push_invitation(%s, %s, %s, %s)",
                (club_id, actor_member_id, invitee_member_id, when))

    clubToJoin = club.models.Club.objects.get(pk=club_id)
    if not clubToJoin:
        logger.debug("Club '%s' does not exist", (club_id))
        return

    sendingMember = member.models.Member.objects.get(pk=actor_member_id)
    if not sendingMember:
        logger.debug("Actor '%s' does not exist", (actor_member_id))
        return

    receivingMember = member.models.Member.objects.get(pk=invitee_member_id)
    if not receivingMember:
        logger.debug("Invitee '%s' does not exist", (invitee_member_id))
        return

    # TODO - Check datetime
    to = receivingMember.device_token
    # TODO: Localize
    template = Template(settings.PUSH_INVITE_TEXT)
    message = template.substitute(senderName=sendingMember.name,
                                  clubName=clubToJoin.name,
                                  clubUrlName=quote_plus(clubToJoin.name))
    payload = {'owner_id': actor_member_id,
               'club_id': club_id,
               'type': 'invite'}
    result = send_push_message(to, message, payload)
    logger.info("Event handled: send_push_message(%s, %s, %s) = %s",
                (to, message, payload, result))


@shared_task
def send_push_joined(club_id, sender_member_id, receiver_member_id):
    logger.info("Event received: send_joined_notice(%s, %s, %s)",
                (club_id, sender_member_id, receiver_member_id))

    joinedClub = club.models.Club.objects.get(pk=club_id)
    if not joinedClub:
        logger.debug("Club '{}' does not exist".format(club_id))
        return

    sendingMember = member.models.Member.objects.get(pk=sender_member_id)
    if not sendingMember:
        logger.debug("Sender '{}' does not exist".format(sender_member_id))
        return

    receivingMember = member.models.Member.objects.get(pk=receiver_member_id)
    if not receivingMember:
        logger.debug("Receiver '{}' does not exist".format(receiver_member_id))
        return

    to = receivingMember.device_token
    # TODO: Localize
    template = Template(settings.PUSH_JOIN_TEXT)
    message = template.substitute(senderName=sendingMember.name,
                                  clubName=joinedClub.name,
                                  clubUrlName=quote_plus(joinedClub.name))
    result = send_push_message(to, message)
    logger.info("Event handled: send_push_message(%s, %s) = %s",
                (to, message, result))


@shared_task
def send_push_status_update(club_id, sender_member_id, receiver_member_id,
                            when):
    logger.info("Event received: send_push_status_update(%s, %s, %s, %s)",
                (club_id, sender_member_id, receiver_member_id, when))

    updatedClub = club.models.Club.objects.get(pk=club_id)
    if not updatedClub:
        logger.debug("Club '%s' does not exist", (club_id))
        return

    sendingMember = member.models.Member.objects.get(pk=sender_member_id)
    if not sendingMember:
        logger.debug("Sender '%s' does not exist", (sender_member_id))
        return

    receivingMember = member.models.Member.objects.get(pk=receiver_member_id)
    if not receivingMember:
        logger.debug("Receiver '%s' does not exist", (receiver_member_id))
        return

    to = receivingMember.device_token
    # TODO: Localize
    template = Template(settings.PUSH_UPDATE_TEXT)
    message = template.substitute(senderName=sendingMember.name,
                                  clubName=updatedClub.name,
                                  clubUrlName=quote_plus(updatedClub.name))
    payload = {'owner_id': sender_member_id,
               'club_id': club_id,
               'type': 'update'}
    result = send_push_message(to, message, payload)
    logger.info("Event handled: send_push_message(%s, %s, %s) = %s",
                (to, message, payload, result))


@shared_task
def send_moji_sms_invitation(actor_member_id, emoji, invitee_sms_number, when):
    logger.info("Event received: send_moji_sms_invitation({}, {}, {}, {})"
                .format(actor_member_id, emoji, invitee_sms_number, when))

    to = validate_sms_number(invitee_sms_number)
    if not to:
        logger.debug("SMS target '{}' is invalid".format(invitee_sms_number))
        return

    sendingMember = member.models.Member.objects.get(pk=actor_member_id)
    if not sendingMember:
        logger.debug("Actor '{}' does not exist".format(actor_member_id))
        return

    # TODO - Check datetime

    # TODO: Localize
    template = Template(settings.MOJI_SMS_INVITE_TEXT)
    message = template.substitute(senderName=sendingMember.name,
                                  emoji=emoji)
    result = send_unicode_message(to, message)
    logger.info("Event handled: send_moji_sms_invitation({}, {}) {}" .format(
        to, message, result))


def validate_sms_number(sms_number):
    """Expects numeric, with an optional leading + symbol, which it returns"""
    match = re.match("^(\+?)(\d+)$", sms_number)
    if match:
        return '+' + match.group(2)
    return False
