from django.db import models

from django_extensions.db.models import TimeStampedModel
from author.decorators import with_author

from expressmanage.utils import normalize_string


@with_author
class Customer(TimeStampedModel):
    name            = models.CharField(max_length=255)
    firm            = models.CharField(max_length=80)
    address         = models.CharField(max_length=255, blank=True, null=True)
    city            = models.CharField(max_length=50, blank=True, null=True)
    mobile_number   = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = normalize_string(self.name)
        self.firm = normalize_string(self.firm)
        self.address = normalize_string(self.address)
        self.city = normalize_string(self.city)
        super(Customer, self).save(*args, **kwargs)

# self._state.adding is True creating
# self._state.adding is False updating