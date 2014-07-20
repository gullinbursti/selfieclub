from statusupdate import serializers
from statusupdate import models
from rest_framework import viewsets


class StatusUpdate(viewsets.ReadOnlyModelViewSet):
    queryset = models.StatusUpdate.objects.all()
    serializer_class = serializers.StatusUpdate
