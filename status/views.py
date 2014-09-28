from status import serializers
from status import models
from rest_framework import viewsets


class StatusUpdate(viewsets.ReadOnlyModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-public-methods, too-many-ancestors
    queryset = models.StatusUpdate.objects.all()
    serializer_class = serializers.StatusUpdate
