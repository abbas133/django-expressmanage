from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from django.http import HttpResponseRedirect

from .models import Invoice, InvoiceLineItem, Payment, Receipt
from .forms import PaymentForm, LotPaymentForm

from expressmanage.orders.models import InwardOrder

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


class LotPayment_CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.FormView):
    raise_exception = True
    permission_required = ('invoices.add_payment')

    template_name = 'payments/lot_payment.html'
    form_class = LotPaymentForm
    success_url = reverse_lazy('invoices:payment_index')

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        customer = form.cleaned_data['customer']
        inward_order = form.cleaned_data['lot_number']
        amount = form.cleaned_data['amount']

        order_invoices = Invoice.objects.filter(inward_order=inward_order)

        for invoice in order_invoices:
            invoice_payment = Payment()
            invoice_payment.customer = customer
            invoice_payment.invoice = invoice

            if amount > 0:
                if amount > invoice.pending_amount:
                    invoice_payment.amount = invoice.pending_amount
                    amount = amount - invoice.pending_amount
                else:
                    invoice_payment.amount = amount
                    amount = 0
                invoice_payment.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    # def get_sucess_url(self):
    #     return reverse_lazy('invoices:payment_index')

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


def load_customer_inward_orders(request):
    customer_id = request.GET.get('cid')
    inward_orders = InwardOrder.objects.filter(customer=customer_id, status='Active')
    return render(request, 'payments/filtered_inward_orders.html', {'filtered_inward_orders': inward_orders})


def fetch_invoice_details(request):
    invoice_id = request.GET.get('inv_id')
    invoice = Invoice.objects.get(pk=invoice_id)
    return JsonResponse({'pending_amount' : invoice.pending_amount})


def load_order_amount_pending(request):
    inward_order_id = request.GET.get('inv_id')
    return JsonResponse({'pending_amount': Invoice.objects.filter(inward_order=inward_order_id).aggregate(Sum('pending_amount'))['pending_amount__sum']})