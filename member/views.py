from club import models as club_model
from club import serializers as club_serializers
from django.db.models import Q
from member import models
from member import serializers
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response


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
            response = queryset.filter(
                Q(clubmember__user=member_id) | Q(owner=member_id))
        else:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        return response
