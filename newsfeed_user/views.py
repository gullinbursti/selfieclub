from newsfeed_user import serializers
from newsfeed_user import models
from rest_framework import viewsets


class NewsfeedType(viewsets.ReadOnlyModelViewSet):
    queryset = models.NewsfeedType.objects.all()
    serializer_class = serializers.NewsfeedType


class Newsfeed(viewsets.ReadOnlyModelViewSet):
    queryset = models.Newsfeed.objects.all()
    serializer_class = serializers.Newsfeed
