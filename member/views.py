from member import serializers
from member import models
from rest_framework import viewsets


class Member(viewsets.ReadOnlyModelViewSet):
    queryset = models.Member.objects.all()
    serializer_class = serializers.Member
    # paginate_by = 10
    # max_paginate_by = 50
