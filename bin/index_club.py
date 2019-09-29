import django
from club import tasks
from club import models

django.setup()
for club in models.Club.objects.all():
    tasks.index_club(club.id)
