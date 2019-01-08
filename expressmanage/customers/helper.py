from django.db.models import Sum

from expressmanage.orders.models import InwardOrder, OutwardOrder
from expressmanage.invoices.models import Invoice, Payment


class CustomerSummary:
    def get_recent_invoices(customer):
        return Invoice.objects.filter(inward_order__customer=customer.pk).order_by("created")

    def get_active_lots(customer):
        return InwardOrder.objects.filter(customer=customer.pk, status="Active").count()

    def get_active_invoices(customer):
        return Invoice.objects.filter(inward_order__customer=customer.pk, status="Active").count()

    def get_pending_amount(customer):
        return Invoice.objects.filter(inward_order__customer=customer.pk, status="Active").aggregate(Sum('pending_amount'))['pending_amount__sum']