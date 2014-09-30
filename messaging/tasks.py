"""Handle Celery tasks related to messaging via SMS or Push."""

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


LOGGER = get_task_logger(__name__)


@shared_task
def send_sms_invitation(club_id, actor_member_id, invitee_sms_number, when):
    """Send sms invitation."""
    LOGGER.info("Event received: send_sms_invitation(%s, %s, %s, %s)",
                club_id, actor_member_id, invitee_sms_number, when)

    recipient = validate_sms_number(invitee_sms_number)
    if not recipient:
        LOGGER.debug("SMS target '%s' is invalid", invitee_sms_number)
        return

    club_to_join = club.models.Club.objects.get(pk=club_id)
    if not club_to_join:
        LOGGER.debug("Club '%s' does not exist", club_id)
        return

    sending_member = member.models.Member.objects.get(pk=actor_member_id)
    if not sending_member:
        LOGGER.debug("Actor '%s' does not exist", actor_member_id)
        return

    # TODO - Check datetime

    # TODO: Localize
    template = Template(settings.SMS_INVITE_TEXT)
    club_url_name = quote_plus(club_to_join.name)
    message = template.substitute(senderName=sending_member.name,
                                  clubName=club_to_join.name,
                                  clubUrlName=club_url_name)
    result = send_sms_message(recipient, message)
    LOGGER.info("Event handled: send_sms_invitation(%s, %s) %s",
                recipient, message, result)


@shared_task
def send_sms_thanks(thankee_sms_number):
    """Send sms thanks."""
    LOGGER.info("Event received: send_sms_thanks(%s)", thankee_sms_number)

    recipient = validate_sms_number(thankee_sms_number)
    if not recipient:
        LOGGER.debug("SMS target '%s' is invalid", thankee_sms_number)
        return

    message = settings.SMS_THANKS_TEXT
    result = send_sms_message(recipient, message)
    LOGGER.info("Event handled: sms_thanks(%s, %s) %s",
                recipient, message, result)


@shared_task
def send_push_invitation(club_id, actor_member_id, invitee_member_id, when):
    """Send invitation push message."""
    LOGGER.info("Event received: send_push_invitation(%s, %s, %s, %s)",
                club_id, actor_member_id, invitee_member_id, when)

    club_to_join = club.models.Club.objects.get(pk=club_id)
    if not club_to_join:
        LOGGER.debug("Club '%s' does not exist", club_id)
        return

    sending_member = member.models.Member.objects.get(pk=actor_member_id)
    if not sending_member:
        LOGGER.debug("Actor '%s' does not exist", actor_member_id)
        return

    receiving_member = member.models.Member.objects.get(pk=invitee_member_id)
    if not receiving_member:
        LOGGER.debug("Invitee '%s' does not exist", invitee_member_id)
        return

    # TODO - Check datetime
    recipient = receiving_member.device_token
    # TODO: Localize
    template = Template(settings.PUSH_INVITE_TEXT)
    club_url_name = quote_plus(club_to_join.name)
    message = template.substitute(senderName=sending_member.name,
                                  clubName=club_to_join.name,
                                  clubUrlName=club_url_name)
    payload = {'owner_id': actor_member_id,
               'club_id': club_id,
               'type': 'invite'}
    result = send_push_message(recipient, message, payload)
    LOGGER.info("Event handled: send_push_message(%s, %s, %s) = %s",
                recipient, message, payload, result)


@shared_task
def send_push_joined(club_id, sender_member_id, receiver_member_id):
    """Send 'joined' push message."""
    LOGGER.info("Event received: send_joined_notice(%s, %s, %s)",
                club_id, sender_member_id, receiver_member_id)

    joined_club = club.models.Club.objects.get(pk=club_id)
    if not joined_club:
        LOGGER.debug("Club '%s' does not exist", club_id)
        return

    sending_member = member.models.Member.objects.get(pk=sender_member_id)
    if not sending_member:
        LOGGER.debug("Sender '%s' does not exist", sender_member_id)
        return

    receiving_member = member.models.Member.objects.get(pk=receiver_member_id)
    if not receiving_member:
        LOGGER.debug("Receiver '%s' does not exist", receiver_member_id)
        return

    recipient = receiving_member.device_token
    # TODO: Localize
    template = Template(settings.PUSH_JOIN_TEXT)
    club_url_name = quote_plus(joined_club.name)
    message = template.substitute(senderName=sending_member.name,
                                  clubName=joined_club.name,
                                  clubUrlName=club_url_name)
    result = send_push_message(recipient, message)
    LOGGER.info("Event handled: send_push_message(%s, %s) = %s",
                recipient, message, result)


@shared_task
def send_push_status_update(club_id, sender_member_id, receiver_member_id,
                            when):
    """Send 'status update' push message."""
    LOGGER.info("Event received: send_push_status_update(%s, %s, %s, %s)",
                club_id, sender_member_id, receiver_member_id, when)

    updated_club = club.models.Club.objects.get(pk=club_id)
    if not updated_club:
        LOGGER.debug("Club '%s' does not exist", club_id)
        return

    sending_member = member.models.Member.objects.get(pk=sender_member_id)
    if not sending_member:
        LOGGER.debug("Sender '%s' does not exist", sender_member_id)
        return

    receiving_member = member.models.Member.objects.get(pk=receiver_member_id)
    if not receiving_member:
        LOGGER.debug("Receiver '%s' does not exist", receiver_member_id)
        return

    recipient = receiving_member.device_token
    # TODO: Localize
    template = Template(settings.PUSH_UPDATE_TEXT)
    club_url_name = quote_plus(updated_club.name)
    message = template.substitute(senderName=sending_member.name,
                                  clubName=updated_club.name,
                                  clubUrlName=club_url_name)
    payload = {'owner_id': sender_member_id,
               'club_id': club_id,
               'type': 'update'}
    result = send_push_message(recipient, message, payload)
    LOGGER.info("Event handled: send_push_message(%s, %s, %s) = %s",
                recipient, message, payload, result)


@shared_task
def send_moji_sms_invitation(actor_member_id, emoji, invitee_sms_number, when):
    """Send moji invitation via SMS."""
    LOGGER.info("Event received: send_moji_sms_invitation(%s, %s, %s, %s)",
                actor_member_id, emoji, invitee_sms_number, when)

    recipient = validate_sms_number(invitee_sms_number)
    if not recipient:
        LOGGER.debug("SMS target '%s' is invalid", invitee_sms_number)
        return

    sending_member = member.models.Member.objects.get(pk=actor_member_id)
    if not sending_member:
        LOGGER.debug("Actor '%s' does not exist", actor_member_id)
        return

    # TODO - Check datetime

    # TODO: Localize
    template = Template(settings.MOJI_SMS_INVITE_TEXT)
    message = template.substitute(senderName=sending_member.name,
                                  emoji=emoji)
    result = send_unicode_message(recipient, message)
    LOGGER.info("Event handled: send_moji_sms_invitation(%s, %s) %s",
                recipient, message, result)


def validate_sms_number(sms_number):
    """Expect numeric, with an optional leading + symbol, which it returns."""
    match = re.match(r"^(\+?)(\d+)$", sms_number)
    if match:
        return '+' + match.group(2)
    return False
