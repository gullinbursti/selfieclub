from newsfeed_user import serializers
from newsfeed_user import models
from rest_framework import viewsets


class NewsfeedType(viewsets.ReadOnlyModelViewSet):
    queryset = models.NewsfeedType.objects.all()
    serializer_class = serializers.NewsfeedType


class NewsfeedEvent(viewsets.ReadOnlyModelViewSet):
    queryset = models.NewsfeedEvent.objects.all()
    serializer_class = serializers.NewsfeedEvent
