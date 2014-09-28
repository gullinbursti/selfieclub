from media.serializers import UploadInstructionsRequestSerializer
from media.serializers import UploadInstructionsResponseSerializer
from media.services import UploadInstructionsService
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UploadInstructions(APIView):
    def post(self, request, format=None):
        request_serializer = UploadInstructionsRequestSerializer(
            data=request.DATA)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        response = UploadInstructionsService() \
            .process(**request_serializer.data)
        response_serializer = UploadInstructionsResponseSerializer(response)
        rest_response = Response(response_serializer.data,
                                 status=status.HTTP_200_OK)

        return rest_response
