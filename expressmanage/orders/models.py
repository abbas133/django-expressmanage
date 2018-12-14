from django.db import models

from django_extensions.db.models import TimeStampedModel
from author.decorators import with_author

from expressmanage.customers.models import Customer
from expressmanage.products.models import Product, ContainerType

from datetime import datetime


# INWARD ORDER
# ------------------------------------------------------------------------------
@with_author
class InwardOrder(TimeStampedModel):
    # Status choices
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    STATUS_CHOICES = (
        (ACTIVE, ACTIVE),
        (INACTIVE, INACTIVE),
    )

    # Chamber choices
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    CHAMBER_CHOICES = (
        (ONE, ONE),
        (TWO, TWO),
        (THREE, THREE),
        (FOUR, FOUR),
    )

    lot_number  = models.CharField(max_length=10, blank=True)
    date        = models.DateTimeField(auto_now_add=False, auto_now=False, default=datetime.now)
    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status      = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)
    chamber     = models.CharField(max_length=50, choices=CHAMBER_CHOICES, default=ONE)

    def __str__(self):
        return self.lot_number

    def save(self, *args, **kwargs):
        # Save to generate PK
        super(InwardOrder, self).save(*args, **kwargs)

        # Lot number composition
        self.lot_number = self.customer.first_name[0].upper() + self.customer.last_name[0].upper() + '00' + str(self.pk)

        super(InwardOrder, self).save(*args, **kwargs)


@with_author
class InOli(TimeStampedModel):
    inward_order    = models.ForeignKey(InwardOrder, on_delete=models.CASCADE)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    container_type  = models.ForeignKey(ContainerType, on_delete=models.CASCADE)
    quantity        = models.IntegerField(default=0)
    stock           = models.IntegerField(default=0)

    def __str__(self):
        return str(self.product.name)

    # self._state.adding is True creating
    # self._state.adding is False updating
    def save(self, *args, **kwargs):
        # Initially stock and quantity would be same
        if self._state.adding is True:
            self.stock = self.quantity

        super(InOli, self).save(*args, **kwargs)


# OUTWARD ORDER
# ------------------------------------------------------------------------------
@with_author
class OutwardOrder(TimeStampedModel):
    # Status choices
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    STATUS_CHOICES = (
        (ACTIVE, ACTIVE),
        (INACTIVE, INACTIVE),
    )

    customer        = models.ForeignKey(Customer, on_delete=models.CASCADE)
    inward_order    = models.ForeignKey(InwardOrder, on_delete=models.CASCADE)
    date            = models.DateTimeField(auto_now_add=False, auto_now=False, default=datetime.now)
    received_by     = models.CharField(max_length=50, default='Self')
    status          = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return str(self.inward_order.lot_number)

    def save(self, *args, **kwargs):
        super(OutwardOrder, self).save(*args, **kwargs)


@with_author
class OutOli(TimeStampedModel):
    outward_order   = models.ForeignKey(OutwardOrder, on_delete=models.CASCADE)
    in_oli          = models.ForeignKey(InOli, on_delete=models.CASCADE, blank=True)
    quantity        = models.IntegerField(default=0)

    def __str__(self):
        return str(self.outward_order.inward_order.lot_number)

    def save(self, *args, **kwargs):
        super(OutOli, self).save(*args, **kwargs)

        in_oli = InOli.objects.get(pk=self.in_oli.pk)
        in_oli.stock -= self.quantity
        in_oli.save()