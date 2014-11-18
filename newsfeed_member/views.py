from newsfeed_member import serializers
from newsfeed_member import models
from rest_framework import viewsets


class NewsfeedType(viewsets.ReadOnlyModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-public-methods, too-many-ancestors
    queryset = models.NewsfeedType.objects.all()
    serializer_class = serializers.NewsfeedType


class Newsfeed(viewsets.ReadOnlyModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-public-methods, too-many-ancestors
    serializer_class = serializers.Newsfeed
    model = models.Newsfeed

    def get_queryset(self):
        queryset = models.Newsfeed.objects.all()
        member_id = self.request.QUERY_PARAMS.get('member_id', None)
        if member_id is not None:
            queryset = queryset.filter(member_id=member_id).order_by('-time')
        return queryset
