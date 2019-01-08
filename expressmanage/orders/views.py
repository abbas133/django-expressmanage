from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render
from django.forms.models import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect

from expressmanage.invoices.models import Invoice

from .models import InwardOrder, OutwardOrder, OutOli
from .forms import InwardOrderForm, InOliFormSet, InOliUpdateFormset, InOliResultFormSet, OutwardOrderForm, OutOliForm, OutOliFormSet
from .helpers import get_invoice, populate_invoice, get_oli_invoice_li, get_out_olis, get_order_invoices, get_order_amount_received, get_order_amount_pending, get_order_amount_total


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
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        outward_orders = get_out_olis(self.object)
        order_invoices = get_order_invoices(self.object)
        order_amount = get_order_amount_total(self.object)
        amount_received = get_order_amount_received(self.object)
        amount_pending = get_order_amount_pending(self.object)

        return self.render_to_response(
            self.get_context_data(
                outward_orders=outward_orders,
                order_invoices=order_invoices,
                order_amount=order_amount,
                amount_received=amount_received,
                amount_pending=amount_pending
            )
        )


class InwardOrder_CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    raise_exception = True
    permission_required = ('orders.add_inwardorder')

    model = InwardOrder
    form_class = InwardOrderForm
    template_name = 'orders/inward_orders/edit.html'
    object = None

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        in_oli_formset = InOliFormSet()

        return self.render_to_response(
            self.get_context_data(form=form, in_oli_formset=in_oli_formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        in_oli_formset = InOliFormSet(self.request.POST)

        if form.is_valid() and in_oli_formset.is_valid():
            return self.form_valid(form, in_oli_formset)
        else:
            return self.form_invalid(form, in_oli_formset)

    def form_valid(self, form, in_oli_formset):
        self.object = form.save(commit=False)
        self.object.save()

        in_olis = in_oli_formset.save(commit=False)
        for oli in in_olis:
            oli.inward_order = self.object
            oli.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, in_oli_formset):
        return self.render_to_response(
            self.get_context_data(form=form, in_oli_formset=in_oli_formset)
        )

    def get_success_url(self):
        return reverse_lazy('orders:in_detail', kwargs={'pk': self.object.pk})


class InwardOrder_UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    raise_exception = True
    permission_required = ('orders.change_inwardorder')

    model = InwardOrder
    form_class = InwardOrderForm
    template_name = 'orders/inward_orders/edit.html'
    object = None

    def get_object(self, queryset=None):
        self.object = super(InwardOrder_UpdateView, self).get_object()
        return self.object

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        in_oli_formset = InOliUpdateFormset(instance=self.object)

        return self.render_to_response(
            self.get_context_data(form=InwardOrderForm(instance=self.object), in_oli_formset=in_oli_formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = InwardOrderForm(data=self.request.POST, instance=self.object)
        in_oli_formset = InOliUpdateFormset(data=self.request.POST, instance=self.object)

        if form.is_valid() and in_oli_formset.is_valid():
            return self.form_valid(form, in_oli_formset)
        else:
            return self.form_invalid(form, in_oli_formset)

    def form_valid(self, form, in_oli_formset):
        self.object = form.save(commit=False)
        self.object.save()

        in_olis = in_oli_formset.save(commit=False)
        for oli in in_olis:
            oli.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, in_oli_formset):
        return self.render_to_response(
            self.get_context_data(form=form, in_oli_formset=in_oli_formset)
        )

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
    form_class = OutwardOrderForm
    template_name = 'orders/outward_orders/edit.html'
    object = None

    def get_context_data(self, **kwargs):
        context = super(OutwardOrder_CreateView, self).get_context_data(**kwargs)
        context['is_invalid'] = kwargs['is_invalid']
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        return self.render_to_response(
            self.get_context_data(form=form, is_invalid=False)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        out_oli_formset = OutOliFormSet(self.request.POST)
        in_order_results = InOliResultFormSet(self.request.POST)

        if form.is_valid() and out_oli_formset.is_valid():
            return self.form_valid(form, out_oli_formset)
        else:
            return self.form_invalid(form, in_order_results, out_oli_formset)

    def form_valid(self, form, out_oli_formset):
        self.object = form.save(commit=False)
        self.object.save()

        invoice = get_invoice(self.object)
        invoice.save()

        out_olis = out_oli_formset.save(commit=False)

        invoice_lis = []
        for oli in out_olis:
            oli.outward_order = self.object
            oli.save()

            invoice_li = get_oli_invoice_li(invoice, oli)
            invoice_li.save()

            invoice_lis.append(invoice_li)

        invoice = populate_invoice(invoice, invoice_lis)
        invoice.save()

        return HttpResponseRedirect(self.get_success_url())


    def form_invalid(self, form, in_order_results, out_oli_formset):
        return self.render_to_response(
            self.get_context_data(form=form, in_order_results=in_order_results, out_oli_formset=out_oli_formset, is_invalid=True)
        )

    def get_success_url(self):
        return reverse_lazy('invoices:invoice_detail', kwargs={'pk': Invoice.objects.get(outward_order=self.object.pk).pk})


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
    inward_orders = InwardOrder.objects.filter(customer=customer_id, status='Active').order_by('date')
    return render(request, 'orders/filtered_inorder_options.html', {'filtered_inward_orders': inward_orders})


def load_order_olis(request):
    in_order_id = request.GET.get('inid')
    in_order_results = InOliResultFormSet(instance=InwardOrder.objects.get(pk=in_order_id))

    out_oli_formset = inlineformset_factory(
        OutwardOrder,
        OutOli,
        can_delete=False,
        extra=len(in_order_results),
        form=OutOliForm
    )
    return render(request, 'orders/filtered_oli_options.html', {'in_order_results': in_order_results, 'out_oli_formset': out_oli_formset})