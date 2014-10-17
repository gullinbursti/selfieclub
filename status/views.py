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
        if 'status_update_id' in self.kwargs:
            update_id = self.kwargs['status_update_id']
            queryset = models.StatusUpdate.objects.filter(id=update_id)
        else:
            queryset = models.StatusUpdate.objects.all()
        return queryset


class StatusUpdateViewers(viewsets.ModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-public-methods, too-many-ancestors
    serializer_class = serializers.StatusUpdateViewerSerializer
    model = models.StatusUpdateViewer
    lookup_field = 'id'

    def get_queryset(self):
        # TODO: validate status_update_id
        status_update_id = self.kwargs['status_update_id']
        return models.StatusUpdateViewer.objects.filter(
            status_update=status_update_id)

    def create(self, request, *args, **kwargs):
        # Always validate first!!!  This lets the serializer do the work.
        member_id = request.DATA['member_id'] \
            if 'member_id' in request.DATA else None
        status_update_id = self.kwargs['status_update_id'] \
            if 'status_update_id' in self.kwargs else None
        serializer = self.get_serializer(
            data={
                'member_id': member_id,
                'status_update_id': status_update_id})
        if not serializer.is_valid():
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        # Check for dups
        # TODO: make sure that status updates exists first
        if self.get_queryset().filter(member=member_id):
            return Response(status=status.HTTP_409_CONFLICT)
        # Save!
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
