from newsfeed_user import serializers
from newsfeed_user import models
from rest_framework import viewsets


class NewsfeedType(viewsets.ReadOnlyModelViewSet):
    queryset = models.NewsfeedType.objects.all()
    serializer_class = serializers.NewsfeedType


class Newsfeed(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.Newsfeed
    model = models.Newsfeed

    def get_queryset(self):
        queryset = models.Newsfeed.objects.all()
        member_id = self.request.QUERY_PARAMS.get('member_id', None)
        if member_id is not None:
            queryset = queryset.filter(user_id=member_id)
        return queryset
