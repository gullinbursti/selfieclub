from member import models
from rest_framework import serializers


# TODO - Pull avatar_url
class Member(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ('id', 'username')
