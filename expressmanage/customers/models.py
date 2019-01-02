from django.db import models

from django_extensions.db.models import TimeStampedModel
from author.decorators import with_author


@with_author
class Customer(TimeStampedModel):
    # first_name      = models.CharField(max_length=50)
    # last_name       = models.CharField(max_length=50, blank=True, null=True)
    name            = models.CharField(max_length=255)
    firm            = models.CharField(max_length=80, blank=True, null=True)
    address         = models.CharField(max_length=255, blank=True, null=True)
    city            = models.CharField(max_length=50, blank=True, null=True)
    mobile_number   = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

# self._state.adding is True creating
# self._state.adding is False updating