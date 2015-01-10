from club import models as club_model
from club import serializers as club_serializers
from datetime import datetime
from django.db.models import Q
from django.db.models import Sum
from member import models
from member import serializers
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from selfieclub.exceptions import BadRequestException
from status import models as status_models
from status import serializers as status_serializers


class Member(viewsets.ReadOnlyModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-ancestors, too-few-public-methods
    queryset = models.Member.objects.all()
    serializer_class = serializers.Member
    # paginate_by = 10
    # max_paginate_by = 50


class MemberClubs(mixins.ListModelMixin, viewsets.GenericViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-ancestors, too-few-public-methods
    queryset = club_model.Club.objects
    serializer_class = club_serializers.Club

    def get_queryset(self):
        queryset = club_model.Club.objects
        member_id = self.kwargs['member_id']
        if member_id is not None:
            # Note that club_member.joined is set to '0000-00-00 00:00:00' if
            # the member has not actually joined the club.  '0000-00-00
            # 00:00:00' is an invalid date and time.  Searching greater then
            # '0001-01-01'.
            response = queryset.filter(
                (Q(clubmember__user=member_id)
                 & Q(clubmember__joined__gte=datetime(1, 1, 1)))
                | Q(owner=member_id))
        else:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        return response


class MemberStatusUpdates(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-ancestors, too-few-public-methods
    queryset = status_models.StatusUpdate.objects
    serializer_class = status_serializers.ExpandedStatusUpdate

    def get_queryset(self):
        queryset = status_models.StatusUpdate.objects
        member_id = self.kwargs['member_id']
        sort_by = self.request.QUERY_PARAMS.get('sort_by', 'updated')
        if member_id and sort_by in ('updated', 'vote_score'):
            response = queryset.filter(creator_id=member_id).filter(parent=0) \
                .exclude(subject='__FLAG__') \
                .annotate(vote_score=Sum('statusupdatevoter__vote')) \
                .order_by('-{}'.format(sort_by))
        else:
            raise BadRequestException()
        return response
