from django.views import generic
from django.urls import reverse_lazy
from django.db import transaction
from django.shortcuts import render
from django.forms.models import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from expressmanage.invoices.models import Invoice, InvoiceLineItem

from .models import InwardOrder, InOli, OutwardOrder, OutOli
from .forms import InOliFormSet, OutOliFormSet, InOliResultFormSet
from .helpers import get_invoice, populate_invoice, get_oli_invoice_li


# INWARD ORDERS
# ------------------------------------------------------------------------------
class InwardOrder_IndexView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    raise_exception = True
    permission_required = ('orders.view_inwardorder')

    template_name = 'orders/inward_orders/index.html'

    def get_queryset(self):
        return InwardOrder.objects.all()


class InwardOrder_DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    raise_exception = True
    permission_required = ('orders.view_inwardorder')

    model = InwardOrder
    template_name = 'orders/inward_orders/detail.html'


class InwardOrder_CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    raise_exception = True
    permission_required = ('orders.add_inwardorder')

    model = InwardOrder
    fields = ['customer', 'date', 'chamber']
    template_name = 'orders/inward_orders/edit.html'

    def get_context_data(self, **kwargs):
        context = super(InwardOrder_CreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['inward_olis'] = InOliFormSet(self.request.POST)
        else:
            context['inward_olis'] = InOliFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        inward_olis = context['inward_olis']

        if form.is_valid() and inward_olis.is_valid():
            with transaction.atomic():
                self.object = form.save()

                inward_olis.instance = self.object
                inward_olis.save()
        return super(InwardOrder_CreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('orders:in_detail', kwargs={'pk': self.object.pk})


class InwardOrder_UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    raise_exception = True
    permission_required = ('orders.change_inwardorder')

    model = InwardOrder
    fields = ['customer', 'date', 'chamber']
    template_name = 'orders/inward_orders/edit.html'

    def get_context_data(self, **kwargs):
        context = super(InwardOrder_UpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['inward_olis'] = InOliFormSet(self.request.POST, instance=self.object)
            context['inward_olis'].full_clean()
        else:
            context['inward_olis'] = InOliFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        inward_olis = context['inward_olis']

        if form.is_valid() and inward_olis.is_valid():
            with transaction.atomic():
                self.object = form.save()

                inward_olis.instance = self.object
                inward_olis.save()
        return super(InwardOrder_UpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('orders:in_detail', kwargs={'pk': self.object.pk})


class InwardOrder_DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    raise_exception = True
    permission_required = ('orders.delete_inwardorder')

    model = InwardOrder
    template_name = 'orders/inward_orders/delete.html'
    success_url = reverse_lazy('orders:in_index')


# OUTWARD ORDERS
# ------------------------------------------------------------------------------
class OutwardOrder_IndexView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    raise_exception = True
    permission_required = ('orders.view_outwardorder')

    template_name = 'orders/outward_orders/index.html'

    def get_queryset(self):
        return OutwardOrder.objects.all()


class OutwardOrder_DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    raise_exception = True
    permission_required = ('orders.view_outwardorder')

    model = OutwardOrder
    template_name = 'orders/outward_orders/detail.html'


class OutwardOrder_CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    raise_exception = True
    permission_required = ('orders.add_outwardorder')

    model = OutwardOrder
    fields = ['customer', 'inward_order', 'date', 'received_by',]
    template_name = 'orders/outward_orders/edit.html'

    def get_context_data(self, **kwargs):
        context = super(OutwardOrder_CreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['outward_olis'] = OutOliFormSet(self.request.POST)

            in_order_instance = InwardOrder.objects.get(pk=self.request.POST['inward_order'])
            context['in_order_results'] = InOliResultFormSet(self.request.POST, instance=in_order_instance)
        else:
            pass
        return context
 
    def form_valid(self, form):
        context = self.get_context_data()
        outward_olis = context['outward_olis']

        if form.is_valid():
            with transaction.atomic():
                self.object = form.save()

                invoice = get_invoice(self.object)
                invoice.save()

                if outward_olis.is_valid():
                    outward_olis.instance = self.object

                    out_olis = self.populate_oli_details(outward_order=outward_olis.instance)
                    # out_olis = OutOli.objects.bulk_create(out_olis)

                    invoice_lis = get_oli_invoice_li(invoice, out_olis)
                    invoice_lis = InvoiceLineItem.objects.bulk_create(invoice_lis)

                    invoice = populate_invoice(invoice, invoice_lis)
                    invoice.save()
        return super(OutwardOrder_CreateView, self).form_valid(form)

    def populate_oli_details(self, outward_order):
    # def populate_oli_details(self, out_olis):
        inoli_set           = 'inoli_set-'
        outoli_set          = 'outoli_set-'

        field_id            = '-id'
        field_quantity      = '-quantity'
        field_stock         = '-stock'

        attr_total_forms    = '-TOTAL_FORMS'

        total_forms = int(self.request.POST[outoli_set.replace('-', '') + attr_total_forms])
        lst_out_olis = []

        for var in list(range(total_forms)):
            out_quantity = int(self.request.POST[outoli_set + str(var) + field_quantity])

            if out_quantity > 0:
                oli = OutOli(
                    outward_order = outward_order,
                    in_oli_id = self.request.POST[inoli_set + str(var) + field_id],
                    quantity = out_quantity
                )

                lst_out_olis.append(oli)
                oli.save()
            else:
                pass
        return lst_out_olis

    def get_success_url(self):
        return reverse_lazy('invoices:invoice_detail', kwargs={'pk': Invoice.objects.get(outward_order=self.object.pk).pk})


# OLI VIEWS - DEVELOPER BACKDOOR
# ------------------------------------------------------------------------------
class InOli_IndexView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    template_name = 'orders/order_line_items/index.html'
    context_object_name = 'in_oli_list'

    def get_queryset(self):
        return InOli.objects.all()


class InOli_DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = InOli
    template_name = 'orders/order_line_items/detail.html'


class OutOli_IndexView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    template_name = 'orders/order_line_items/index.html'
    context_object_name = 'out_oli_list'

    def get_queryset(self):
        return OutOli.objects.all()


class OutOli_DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = OutOli
    template_name = 'orders/order_line_items/detail.html'


# RECEIVING CHALLAN
# ------------------------------------------------------------------------------
class ReceivingChallan_DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    raise_exception = True
    permission_required = ('orders.view_inwardorder')

    model = InwardOrder
    template_name = 'orders/receiving_challan.html'


# AJAX HELPER VIEW
# ------------------------------------------------------------------------------
def load_customer_in_orders(request):
    customer_id = request.GET.get('cid')
    inward_orders = InwardOrder.objects.filter(customer = customer_id).filter(status = 'Active').order_by('date')
    return render(request, 'orders/filtered_inorder_options.html', {'filtered_inward_orders': inward_orders})


def load_order_olis(request):
    in_order_id = request.GET.get('inid')
    in_order_results = InOliResultFormSet(instance=InwardOrder.objects.get(pk=in_order_id))

    outward_olis = inlineformset_factory(
        OutwardOrder,
        OutOli,
        fields=('outward_order', 'quantity',),
        can_delete=False,
        extra=len(in_order_results),
    )
    return render(request, 'orders/filtered_oli_options.html', {'in_order_results': in_order_results, 'outward_olis': outward_olis})