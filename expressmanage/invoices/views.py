from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Invoice, InvoiceLineItem, Payment, Receipt


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
class Payment_IndexView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    raise_exception = True
    permission_required = ('invoices.view_payment')

    template_name = 'payments/index.html'

    def get_queryset(self):
        return Payment.objects.all()


class Payment_CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    raise_exception = True
    permission_required = ('invoices.add_payment')

    model = Payment
    fields = ['invoice', 'amount']
    template_name = 'payments/edit.html'

    def get_success_url(self):
        return reverse_lazy('invoices:payment_index')


# RECEIPT
# ------------------------------------------------------------------------------
class Receipt_IndexView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    raise_exception = True
    permission_required = ('invoices.view_receipt')

    template_name = 'receipts/index.html'

    def get_queryset(self):
        return Receipt.objects.all()


class Receipt_DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    raise_exception = True
    permission_required = ('invoices.view_receipt')

    model = Receipt
    template_name = 'receipts/detail.html'
