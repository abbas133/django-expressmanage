from django.db import models

from django_extensions.db.models import TimeStampedModel
from author.decorators import with_author

from datetime import datetime

from expressmanage.orders.models import InwardOrder, OutwardOrder, OutOli


class Invoice(TimeStampedModel):
    # Status choices
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    STATUS_CHOICES = (
        (ACTIVE, ACTIVE),
        (INACTIVE, INACTIVE),
    )

    inward_order    = models.ForeignKey(InwardOrder, on_delete=models.CASCADE)
    outward_order   = models.ForeignKey(OutwardOrder, on_delete=models.CASCADE)
    date            = models.DateField(auto_now_add=False, default=datetime.today)
    total_amount    = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    received_amount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pending_amount  = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status          = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return self.inward_order.lot_number

    def save(self, *args, **kwargs):
        self.pending_amount = self.total_amount - self.received_amount
        self.status = self.ACTIVE if self.pending_amount > 0 else self.INACTIVE

        super(Invoice, self).save(*args, **kwargs)


class InvoiceLineItem(TimeStampedModel):
    invoice         = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    out_oli         = models.ForeignKey(OutOli, on_delete=models.CASCADE)
    elapsed_days    = models.IntegerField()
    rate            = models.DecimalField(max_digits=5, decimal_places=2)
    amount          = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.invoice.pk)

    def save(self, *args, **kwargs):
        super(InvoiceLineItem, self).save(*args, **kwargs)


class Payment(TimeStampedModel):
    invoice         = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    date            = models.DateField(auto_now=True)
    amount          = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.invoice.pk)

    def save(self, *args, **kwargs):
        super(Payment, self).save(*args, **kwargs)

        invoice = Invoice.objects.get(pk=self.invoice.pk)
        invoice.received_amount = invoice.received_amount + self.amount
        invoice.save()

        Payment.generate_receipt(invoice, self)

    def generate_receipt(invoice, payment):
        receipt = Receipt(invoice=invoice, payment=payment)


class Receipt(TimeStampedModel):
    invoice         = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment         = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super(Receipt, self).save(*args, **kwargs)