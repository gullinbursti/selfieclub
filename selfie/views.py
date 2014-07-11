from selfie import serializers
from selfie import models
from rest_framework import viewsets


class Selfie(viewsets.ReadOnlyModelViewSet):
    queryset = models.Selfie.objects.all()
    serializer_class = serializers.Selfie
