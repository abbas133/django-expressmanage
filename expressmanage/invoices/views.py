from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.http import JsonResponse


from .models import Invoice, InvoiceLineItem, Payment, Receipt
from .forms import PaymentForm


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
    template_name = 'payments/edit.html'
    form_class = PaymentForm

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


# AJAX HELPER VIEW
# ------------------------------------------------------------------------------
def load_customer_invoices(request):
    customer_id = request.GET.get('cid')
    invoices = Invoice.objects.filter(inward_order__customer=customer_id, status='Active')
    return render(request, 'payments/filtered_invoices.html', {'filtered_invoices': invoices})


def fetch_invoice_details(request):
    invoice_id = request.GET.get('inv_id')
    invoice = Invoice.objects.get(pk=invoice_id)
    return JsonResponse({'pending_amount' : invoice.pending_amount})