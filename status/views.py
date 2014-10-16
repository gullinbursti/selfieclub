from status import serializers
from status import models
from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.response import Response
import logging


LOGGER = logging.getLogger(__name__)


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


class StatusUpdateTraffic(viewsets.ModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-public-methods, too-many-ancestors

    # This set up allows the following link to work:
    #  - http://localhost:8000/status/update/7636/traffic/27/
    #
    # Should allow for using PUT, PATCH, and DELETE
    # the key is lookup_field!!
    serializer_class = serializers.StatusUpdateViewerSerializer
    model = models.StatusUpdateViewer
    lookup_field = 'id'

    # If we really wanted to do this right we would override list(), and then
    # only send back and array of member_ids.  I consider this MVP though.  We
    # can stream line later if needed.
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


class StatusUpdateTrafficOld(viewsets.ModelViewSet):
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
        member = request.DATA['member']
        serializer = serializers.StatusUpdateViewerSerializer(
            data={
                'member': member,
                'status_update': update_id,
            })
        if not serializer.is_valid():
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

#        if models.StatusUpdateViewerSerializer.objects.all().filter
#
#
#            try:
#                serializer.save()
#            except Exception as ex:
#                LOGGER.error('BOOM ==> %s', repr(ex))
#            response = Response(status=status.HTTP_201_CREATED)
#        else:
#        return response


    """
    Two different errors in the HTML, happens in sequence:
        1. <StatusUpdateViewer: 13430 7636> is not 
    """
    def create_bad_1(self, request, *args, **kwargs):
        update_id = self.kwargs['update_id']
        data = request.DATA
        member_id = request.DATA['member']
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


    def create_bad_2(self, request, *args, **kwargs):
        update_id = self.kwargs['update_id']
        data = request.DATA
        member_id = data['member']
        viewer = models.StatusUpdateViewer(status_update_id=update_id,
                                           member_id=member_id)
        serializer = serializers.StatusUpdateViewerSerializer(viewer)
        if serializer.is_valid():
            viewer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
