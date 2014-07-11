from member import models
from rest_framework import serializers


# TODO - Pull avatar_url
class Member(serializers.ModelSerializer):
    avatar_url = serializers.URLField(source='img_url', read_only=True)

    class Meta:
        model = models.Member
        fields = ('id', 'avatar_url', 'username')
