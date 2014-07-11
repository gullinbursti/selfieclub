from newsfeed_user import serializers
from newsfeed_user import models
from rest_framework import viewsets


class NewsfeedType(viewsets.ModelViewSet):
    queryset = models.NewsfeedType.objects.all()
    serializer_class = serializers.NewsfeedType


class NewsfeedEvent(viewsets.ModelViewSet):
    queryset = models.NewsfeedEvent.objects.all()
    serializer_class = serializers.NewsfeedEvent
