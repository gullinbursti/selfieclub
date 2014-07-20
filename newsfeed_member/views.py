from newsfeed_member import serializers
from newsfeed_member import models
from rest_framework import viewsets
import logging

logger = logging.getLogger(__name__)


class NewsfeedType(viewsets.ReadOnlyModelViewSet):
    queryset = models.NewsfeedType.objects.all()
    serializer_class = serializers.NewsfeedType


class Newsfeed(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.Newsfeed
    model = models.Newsfeed

    def get_queryset(self):
        logger.error("hello ...   ")

        queryset = models.Newsfeed.objects.all()
        member_id = self.request.QUERY_PARAMS.get('member_id', None)
        if member_id is not None:
            queryset = queryset.filter(member_id=member_id)
        return queryset
