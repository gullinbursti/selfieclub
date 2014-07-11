from club import serializers
from club import models
from rest_framework import viewsets


class ClubType(viewsets.ReadOnlyModelViewSet):
    queryset = models.ClubType.objects.all()
    serializer_class = serializers.ClubType
