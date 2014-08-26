from club import serializers
from club import models
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions


class ClubType(viewsets.ModelViewSet):
    queryset = models.ClubType.objects.all()
    serializer_class = serializers.ClubType


class Club(viewsets.ReadOnlyModelViewSet):
    queryset = models.Club.objects.all()
    serializer_class = serializers.Club


class ClubLabel(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.ClubLabel.objects.all()
    serializer_class = serializers.ClubLabel


class ClubLabelByName(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    model = models.ClubLabel
    serializer_class = serializers.ClubLabel
    lookup_field = 'name'


class ClubsWithLabelByLabelName(mixins.ListModelMixin, viewsets.GenericViewSet):
    # model = models.Club
    queryset = models.Club.objects.all()
    serializer_class = serializers.ClubSummary

    def get_queryset(self):
        queryset = models.Club.objects.all()
        member_id = self.kwargs['label']
        if member_id is not None:
            queryset = queryset.filter(label__name=member_id)
        return queryset
