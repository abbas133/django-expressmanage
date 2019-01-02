from expressmanage.products.models import RateSlab
from expressmanage.invoices.models import Invoice, InvoiceLineItem

def get_oli_elapsed_days(out_oli):
    return (out_oli.outward_order.date - out_oli.in_oli.inward_order.date).days


def get_oli_applicable_rate(out_oli, elapsed_days=None):
    # rate_slabs = RateSlab.objects.filter(container_type=out_oli.in_oli.container_type).order_by("slab_number")
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
        invoice.total_amount = invoice.total_amount + invoice_li.amount

    return invoice


def get_oli_invoice_li(invoice, out_olis):
    invoice_lis = []

    for out_oli in out_olis:
        elapsed_days = get_oli_elapsed_days(out_oli)
        rate = get_oli_applicable_rate(out_oli, elapsed_days)
        amount = out_oli.quantity * rate
        invoice_li = InvoiceLineItem(invoice=invoice, out_oli=out_oli, elapsed_days=elapsed_days, rate=rate, amount=amount)

        invoice_lis.append(invoice_li)

    return invoice_lis