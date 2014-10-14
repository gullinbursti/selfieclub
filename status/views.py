from status import serializers
from status import models
from rest_framework import viewsets


class StatusUpdateViewSet(viewsets.ReadOnlyModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-public-methods, too-many-ancestors
    serializer_class = serializers.StatusUpdate
    model = models.StatusUpdate

    def get_queryset(self):
        if 'pk' in self.kwargs:
            update_id = self.kwargs['pk']
            queryset = models.StatusUpdate.objects.filter(id=update_id)
        else:
            queryset = models.StatusUpdate.objects.all()
        return queryset


class StatusUpdateTraffic(viewsets.ReadOnlyModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-public-methods, too-many-ancestors
    serializer_class = serializers.StatusUpdate
    model = models.StatusUpdate

    def get_queryset(self):
        update_id = self.kwargs['update_id']
        return models.StatusUpdate.objects.filter(id=update_id)
