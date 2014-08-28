from django.db import models


class Callback(models.Model):
    message_id = models.CharField(unique=True, max_length=16)
    # status_id could be, but currently is not, a ForeignKey
    status_id = models.CharField(max_length=9, null=True)
    # error_id could be, but currently is not, a ForeignKey
    error_id = models.SmallIntegerField(null=True)
    source_number = models.CharField(max_length=18)
    source_network = models.CharField(max_length=6, null=True)
    destination_number = models.CharField(max_length=18)
    text = models.CharField(max_length=255)
    callback_timestamp = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_messaging_callback'


class SourceNumber(models.Model):
    id = models.IntegerField(primary_key=True)
    phone_number = models.CharField(unique=True, max_length=12)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'tbl_nexmo_source'


class PoolCounter(models.Model):
    """Not the best place for this, but so far this is the only counter"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=64)
    counter = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_counter'
