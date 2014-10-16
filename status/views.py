from status import serializers
from status import models
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response


class StatusUpdateViewSet(viewsets.ReadOnlyModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-public-methods, too-many-ancestors
    serializer_class = serializers.StatusUpdate
    model = models.StatusUpdate

    def get_queryset(self):
        if 'pk' in self.kwargs:
            update_id = self.kwargs['pk']
            queryset = models.StatusUpdate.objects.filter(id=update_id)
        else:
            queryset = models.StatusUpdate.objects.all()
        return queryset


class StatusUpdateViewers(viewsets.ModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-public-methods, too-many-ancestors
    serializer_class = serializers.StatusUpdateViewerSerializer
    model = models.StatusUpdateViewer

    def get_queryset(self):
        update_id = self.kwargs['update_id']
        return models.StatusUpdateViewer.objects.filter(
            status_update=update_id)

    def create(self, request, *args, **kwargs):
        update_id = self.kwargs['update_id']
        data = request.DATA
        if 'member_id' not in data:
            return False
        member_id = data['member_id']
        viewer = models.StatusUpdateViewer(status_update_id=update_id,
                                           member_id=member_id)
        viewer.save()
        return Response(viewer, status=status.HTTP_201_CREATED)
        # serializer = serializers.StatusUpdateViewerSerializer(viewer)
        # if serializer.is_valid():
        #     viewer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors,
        #                 status=status.HTTP_400_BAD_REQUEST)
