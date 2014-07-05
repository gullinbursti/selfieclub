from activity import models
from activity import serializers
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class User(APIView):
    def get_object(self, id):
        try:
            return models.Activity.objects.get(pk=id)
        except models.Activity.DoesNotExist:
            raise Http404

    def get(self, request, id=None, format=None):
        if id is not None:
            activity = self.get_object(id=id)
            serializer = serializers.Activity(activity)
            return Response(serializer.data)
        else:
            activities = models.Activity.objects.all()
            serializer = serializers.Activity(activities, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.Activity(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id, format=None):
        activity = self.get_object(id)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id, format=None):
        activity = self.get_object(id)
        serializer = serializers.Activity(activity, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
