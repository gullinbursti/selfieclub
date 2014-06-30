from media.serializers import UploadInstructionsRequestSerializer
from media.serializers import UploadInstructionsResponseSerializer
from media.services import UploadInstructionsService
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UploadInstructions(APIView):
    def post(self, request, format=None):
        serializer = UploadInstructionsRequestSerializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tdt = UploadInstructionsService().process(**serializer.data)
        something = UploadInstructionsResponseSerializer(tdt)
        return Response(something.data, status=status.HTTP_201_CREATED)
