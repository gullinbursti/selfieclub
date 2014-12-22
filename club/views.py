from club import models
from club import serializers
from math import cos, radians
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from status import models as status_models
from status import serializers as status_serializers


class ClubType(viewsets.ModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-ancestors, too-few-public-methods
    queryset = models.ClubType.objects.all()
    serializer_class = serializers.ClubType


class Club(viewsets.ReadOnlyModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-ancestors, too-few-public-methods
    serializer_class = serializers.Club
    model = models.Club

    def get_queryset(self):
        lat = self.request.QUERY_PARAMS.get('lat', None)
        lon = self.request.QUERY_PARAMS.get('lon', None)
        # Default to 10 miles
        radius = int(self.request.QUERY_PARAMS.get('radius', 10))

        def bounding(flat, flon, radius):
            # We'll draw a box to search within, with lat1/lon1 as one corner,
            # and lat2/lon2 as the opposite corner.
            lat1 = flat - (radius / 69.172)
            lat2 = flat + (radius / 69.172)
            lon1 = flon - radius / abs(cos(radians(flat)) * 69.172)
            lon2 = flon + radius / abs(cos(radians(flat)) * 69.172)
            return (lat1, lat2, lon1, lon2)

        if lat and lon:
            # Geo-search requires float values
            flat = float(lat)
            flon = float(lon)
            (lat1, lat2, lon1, lon2) = bounding(flat, flon, radius)
            # Pythagorean theorem FTW!
            queryset = models.Club.objects \
                .filter(lat__range=(lat1, lat2),
                        lon__range=(lon1, lon2)) \
                .extra(select={'distance': '\
3956 * 2 * ASIN(SQRT(POWER(SIN((%s - lat) * PI()/180 / 2), 2) + \
COS(%s * PI()/180) * COS(lat * PI()/180) * \
POWER(SIN((%s - lon) * PI()/180 / 2), 2) ))'},
                       select_params=(flat, flat, flon)) \
                .order_by('distance')[:1]
        else:
            queryset = models.Club.objects.all()
        return queryset


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


class ClubStatusUpdates(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-ancestors, too-few-public-methods
    queryset = status_models.StatusUpdate.objects
    serializer_class = status_serializers.ExpandedStatusUpdate

    def get_queryset(self):
        queryset = status_models.StatusUpdate.objects
        club_id = self.kwargs['club_id']
        if club_id:
            response = queryset.filter(club=club_id).filter(parent=0) \
                .exclude(subject='__FLAG__').order_by('-updated')
        else:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        return response
