from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Customer


class Customer_IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'customers/index.html'

    def get_queryset(self):
        return Customer.objects.all()


class Customer_DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    raise_exception = True
    permission_required = ('customers.view_customer')

    model = Customer
    template_name = 'customers/detail.html'

    def get_context_data(self, **kwargs):
        context = super(Customer_DetailView, self).get_context_data(**kwargs)
        context['pending_amount'] = '53269'

        return context


class Customer_CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    raise_exception = True
    permission_required = ('customers.add_customer')

    model = Customer
    fields = ['firm','first_name', 'last_name', 'address', 'city', 'mobile_number']
    template_name = 'customers/edit.html'

    def get_success_url(self):
        return reverse_lazy('customers:customer_detail', kwargs={'pk': self.object.pk})


class Customer_UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    raise_exception = True
    permission_required = ('customers.change_customer')

    model = Customer
    fields = ['firm','first_name', 'last_name', 'address', 'city', 'mobile_number']
    template_name = 'customers/edit.html'

    def get_success_url(self):
        return reverse_lazy('customers:customer_detail', kwargs={'pk': self.object.pk})


class Customer_DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    raise_exception = True
    permission_required = ('customers.delete_customer')

    model = Customer
    template_name = 'customers/delete.html'
    success_url = reverse_lazy('customers:customer_index')