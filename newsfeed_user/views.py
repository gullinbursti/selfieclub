from django import http
from newsfeed_user import serializers
from newsfeed_user import models
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class NewsfeedType(APIView):
    def get_object(self, id):
        try:
            return models.NewsfeedType.objects.get(pk=id)
        except models.NewsfeedType.DoesNotExist:
            raise http.Http404

    def get(self, request, id=None, format=None):
        if id is not None:
            feed_type = self.get_object(id=id)
            serializer = serializers.NewsfeedType(feed_type)
            return Response(serializer.data)
        else:
            newfeed_types = models.NewsfeedType.objects.all()
            serializer = serializers.NewsfeedType(newfeed_types, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.NewsfeedType(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id, format=None):
        feed_type = self.get_object(id)
        feed_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id, format=None):
        feed_type = self.get_object(id)
        serializer = serializers.NewsfeedType(feed_type, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
