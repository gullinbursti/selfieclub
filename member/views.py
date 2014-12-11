from club import models as club_model
from club import serializers as club_serializers
from django.db.models import Q
from member import models
from member import serializers
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from datetime import datetime


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
