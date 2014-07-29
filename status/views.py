from status import serializers
from status import models
from rest_framework import viewsets


class StatusUpdate(viewsets.ReadOnlyModelViewSet):
    queryset = models.StatusUpdate.objects.all()
    serializer_class = serializers.StatusUpdate
