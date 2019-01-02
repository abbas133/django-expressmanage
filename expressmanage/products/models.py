from django.db import models

from django_extensions.db.models import TimeStampedModel
from author.decorators import with_author


@with_author
class Product(TimeStampedModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


@with_author
class ContainerType(TimeStampedModel):
    name            = models.CharField(max_length=50)
    description     = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


@with_author
class RateSlab(TimeStampedModel):
    container_type      = models.ForeignKey(ContainerType, on_delete=models.CASCADE)
    rate                = models.DecimalField(max_digits=5, decimal_places=2)
    number_of_days      = models.IntegerField()
    # slab_number         = models.IntegerField()

    def __str__(self):
        return str(self.pk)


# self._state.adding is True creating
# self._state.adding is False updating