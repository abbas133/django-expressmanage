from django.db import models

from django_extensions.db.models import TimeStampedModel
from author.decorators import with_author


@with_author
class Customer(TimeStampedModel):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    firm            = models.CharField(max_length=80)
    address         = models.CharField(max_length=255)
    city            = models.CharField(max_length=50)
    mobile_number   = models.IntegerField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

# self._state.adding is True creating
# self._state.adding is False updating