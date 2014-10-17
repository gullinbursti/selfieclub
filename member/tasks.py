from __future__ import absolute_import

from celery import shared_task
from celery.utils.log import get_task_logger
from member.models import Member
from member.models import ClubMember


LOGGER = get_task_logger(__name__)


# TODO: Decrypt member_phone from the Member object, stop passing it
@shared_task
def convert_invitations(member_id, member_phone, when):
    LOGGER.info(
        "Event received: convert_invitations(%s, %s, %s)",
        member_id, member_phone, when)

    user = Member.objects.get(pk=member_id)
    if not user:
        LOGGER.debug("Member '%s' does not exist", member_id)
        return

    ClubMember.objects.filter(
        mobile_number=member_phone, pending=1).update(
            user=user)
