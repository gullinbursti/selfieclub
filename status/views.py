from django.utils import timezone
from status import serializers
from status import models
from messaging import tasks
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
import newsfeed_member


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


class StatusUpdateVoters(viewsets.ModelViewSet):
    # pylint exception - inherited from Django parent
    # pylint: disable=too-many-public-methods, too-many-ancestors
    serializer_class = serializers.StatusUpdateVoterSerializer
    model = models.StatusUpdateVoter
    lookup_field = 'id'

    def get_queryset(self):
        status_update_id = self.kwargs['status_update_id']
        return models.StatusUpdateVoter.objects.filter(
            status_update=status_update_id)

    def create(self, request, *args, **kwargs):
        # Defaulting to upvotes
        vote = request.DATA['vote'] if 'vote' in request.DATA else 'up'
        # Client specifies text, we store numeric
        if vote == 'up':
            vote = 1
        elif vote == 'down':
            vote = -1
        else:
            vote = None
        member_id = request.DATA['member_id'] \
            if 'member_id' in request.DATA else None
        status_update_id = self.kwargs['status_update_id'] \
            if 'status_update_id' in self.kwargs else None
        # Do we need to update an existing vote, or create a new one?
        try:
            voter = self.model.objects.get(member=member_id,
                                           status_update_id=status_update_id)
        except self.model.DoesNotExist:
            voter = None
        if voter:
            existing_vote = voter.vote
            serializer = self.get_serializer(
                voter,
                data={
                    'member_id': member_id,
                    'vote': vote,
                    'status_update_id': status_update_id})
        else:
            existing_vote = 0
            serializer = self.get_serializer(
                data={
                    'member_id': member_id,
                    'vote': vote,
                    'status_update_id': status_update_id})
        # Check data validity
        if not serializer.is_valid():
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        status_update = models.StatusUpdate.objects.get(id=status_update_id)
        # We allow votes to change, and keep track
        if serializer.data['vote'] == 'down':
            status_update.votes = status_update.votes - existing_vote - 1
        else:
            status_update.votes = status_update.votes - existing_vote + 1
            if existing_vote < 1:
                # Create newsfeed activity on upvote only
                event = newsfeed_member.models.Newsfeed(
                    member_id=status_update.creator_id,
                    subject_member_id=member_id,
                    status_update_id=status_update_id,
                    club_id=status_update.club_id,
                    event_type_id=5,  # TODO - STATUS_UPVOTED
                    time=timezone.now()
                )
                event.save()
                # Send push on upvote only
                tasks.send_push_voted.delay(member_id, status_update.creator_id)
        status_update.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
