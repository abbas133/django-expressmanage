from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import CustomerForm
from .models import Customer
from .helper import CustomerSummary

class Customer_IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'customers/index.html'

    def get_queryset(self):
        return Customer.objects.all()


class Customer_DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    raise_exception = True
    permission_required = ('customers.view_customer')

    model = Customer
    template_name = 'customers/detail.html'
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        recent_invoices = CustomerSummary.get_recent_invoices(self.object)[:3]
        active_lots = CustomerSummary.get_active_lots(self.object)
        active_invoices = CustomerSummary.get_active_invoices(self.object)
        pending_amount = CustomerSummary.get_pending_amount(self.object)

        return self.render_to_response(
            self.get_context_data(
                recent_invoices=recent_invoices,
                active_lots=active_lots,
                active_invoices=active_invoices,
                pending_amount=pending_amount
            )
        )


class Customer_CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    raise_exception = True
    permission_required = ('customers.add_customer')

    model = Customer
    form_class = CustomerForm
    template_name = 'customers/edit.html'

    def get_success_url(self):
        return reverse_lazy('customers:customer_detail', kwargs={'pk': self.object.pk})


class Customer_UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    raise_exception = True
    permission_required = ('customers.change_customer')

    model = Customer
    form_class = CustomerForm
    template_name = 'customers/edit.html'

    def get_success_url(self):
        return reverse_lazy('customers:customer_detail', kwargs={'pk': self.object.pk})


class Customer_DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    raise_exception = True
    permission_required = ('customers.delete_customer')

    model = Customer
    template_name = 'customers/delete.html'
    success_url = reverse_lazy('customers:customer_index')