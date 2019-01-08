from django.db.models import Sum

from decimal import Decimal

from expressmanage.products.models import RateSlab
from expressmanage.invoices.models import Invoice, InvoiceLineItem, Payment
from expressmanage.orders.models import OutwardOrder, OutOli

def get_oli_elapsed_days(out_oli):
    return (out_oli.outward_order.date - out_oli.in_oli.inward_order.date).days


def get_oli_applicable_rate(out_oli, elapsed_days=None):
    rate_slabs = RateSlab.objects.filter(container_type=out_oli.in_oli.container_type).order_by("number_of_days")
    elapsed_days = elapsed_days if elapsed_days is not None else get_oli_elapsed_days(out_oli)

    for rate_slab in rate_slabs:
        if elapsed_days - rate_slab.number_of_days <= 0:
            return rate_slab.rate
    return rate


def get_invoice(outward_order):
    return Invoice(inward_order=outward_order.inward_order, outward_order=outward_order)


def populate_invoice(invoice, invoice_lis):
    for invoice_li in invoice_lis:
        invoice.total_amount = Decimal(invoice.total_amount) + Decimal(invoice_li.amount)

    return invoice


def get_oli_invoice_li(invoice, out_oli):
    elapsed_days = get_oli_elapsed_days(out_oli)
    rate = get_oli_applicable_rate(out_oli, elapsed_days)
    amount = Decimal(out_oli.quantity) * Decimal(rate)
    invoice_li = InvoiceLineItem(invoice=invoice, out_oli=out_oli, elapsed_days=elapsed_days, rate=rate, amount=amount)

    return invoice_li


def get_out_olis(inward_order):
    return OutOli.objects.filter(in_oli__inward_order=inward_order.pk)


def get_order_invoices(inward_order):
    return Invoice.objects.filter(inward_order=inward_order.pk)


def get_order_amount_total(inward_order):
    return Invoice.objects.filter(inward_order=inward_order.pk).aggregate(Sum('total_amount'))['total_amount__sum']


def get_order_amount_received(inward_order):
    return Invoice.objects.filter(inward_order=inward_order.pk).aggregate(Sum('received_amount'))['received_amount__sum']


def get_order_amount_pending(inward_order):
    return Invoice.objects.filter(inward_order=inward_order.pk).aggregate(Sum('pending_amount'))['pending_amount__sum']