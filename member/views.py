from member import serializers
from member import models
from rest_framework import viewsets


class Member(viewsets.ReadOnlyModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-public-methods, too-many-ancestors
    queryset = models.Member.objects.all()
    serializer_class = serializers.Member
    # paginate_by = 10
    # max_paginate_by = 50
