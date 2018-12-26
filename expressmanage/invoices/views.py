from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Invoice, InvoiceLineItem, Payment


# INVOICE
# -----------------------------------------------------------------------------
class Invoice_IndexView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    raise_exception = True
    permission_required = ('invoices.view_invoice')

    template_name = 'invoices/index.html'

    def get_queryset(self):
        return Invoice.objects.all()


class Invoice_DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    raise_exception = True
    permission_required = ('invoices.view_invoice')

    model = Invoice
    template_name = 'invoices/detail.html'


# PAYMENT
# ------------------------------------------------------------------------------
class Payment_CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    raise_exception = True
    permission_required = ('invoices.add_payment')

    model = Payment
    fields = ['invoice', 'amount']
    template_name = 'payments/edit_modal.html'

    def get_success_url(self):
        return reverse_lazy('invoices:invoice_detail', kwargs={'pk': self.object.invoice.pk})