from expressmanage.orders.models import InwardOrder, OutwardOrder
from expressmanage.invoices.models import Invoice, Payment


class CustomerSummary:
    def get_recent_invoices(customer):
        return Invoice.objects.filter(inward_order__customer=customer.pk).order_by("created")

    def get_active_lots(customer):
        return InwardOrder.objects.filter(customer=customer.pk, status="Active")

    def get_active_invoices(customer):
        return Invoice.objects.filter(inward_order__customer=customer.pk, status="Active")

    def get_pending_amount(customer):
        active_invoices = CustomerSummary.get_active_invoices(customer)

        pending_amount = 0
        for invoice in active_invoices:
            pending_amount += invoice.pending_amount

        return pending_amount