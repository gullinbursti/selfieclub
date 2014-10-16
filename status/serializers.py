from status import models
from django.forms import widgets
from rest_framework import serializers


class StatusUpdate(serializers.ModelSerializer):
    class Meta(object):
        # pylint: disable=too-few-public-methods
        model = models.StatusUpdate
        fields = ('id', 'creator_id', 'is_private', 'votes', 'added')


class StatusUpdateViewerSerializer(serializers.ModelSerializer):
    # Why do this?  The key is 'widget=widgets.TextInput'.  If you try and 
    # load this page through the web browser admin panel you will crash
    # the browser and the site trng to ceate a list for the web form.
    # Check out 'club/serializers.py', I had to do it there.
    #
    # The use of *_id might seem odd, but I THINK the issue with *_id only came
    # in in the model.  Reason for the rename is so thet tha serialiser.errors
    # information matched what is being sent in.  what getting '{"member":
    # ["This field is required."]}' when using the member_id param.  Confusing.
    member_id = serializers.IntegerField(
        widget=widgets.TextInput,
        source='member_id',
        help_text='Enter member_id.')
    status_update_id = serializers.IntegerField(
        widget=widgets.TextInput,
        source='status_update_id',
        help_text='This value is ignored in POSTs, pulled from URL.')

    class Meta(object):
        # pylint: disable=too-few-public-methods
        model = models.StatusUpdateViewer
        fields = ('member_id', 'status_update_id')
