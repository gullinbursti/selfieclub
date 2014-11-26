from club import serializers
from club import models
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions


class ClubType(viewsets.ModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-ancestors, too-few-public-methods
    queryset = models.ClubType.objects.all()
    serializer_class = serializers.ClubType


class Club(viewsets.ReadOnlyModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-ancestors, too-few-public-methods
    queryset = models.Club.objects.all()
    serializer_class = serializers.Club


class ClubLabel(viewsets.ModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-ancestors, too-few-public-methods
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.ClubLabel.objects.all()
    serializer_class = serializers.ClubLabel


class ClubLabelByName(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-ancestors, too-few-public-methods
    model = models.ClubLabel
    serializer_class = serializers.ClubLabel
    lookup_field = 'name'


class ClubsWithLabelByLabelName(mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-ancestors, too-few-public-methods
    # model = models.Club
    queryset = models.Club.objects.all()
    serializer_class = serializers.ClubSummary

    def get_queryset(self):
        queryset = models.Club.objects.all()
        member_id = self.kwargs['label']
        if member_id is not None:
            queryset = queryset.filter(label__name=member_id)
        return queryset
