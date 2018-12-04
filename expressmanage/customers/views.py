from django.views import generic
from django.urls import reverse_lazy

from .models import Customer


class Customer_IndexView(generic.ListView):
    template_name = 'customers/index.html'

    def get_queryset(self):
        return Customer.objects.all()


class Customer_DetailView(generic.DetailView):
    model = Customer
    template_name = 'customers/detail.html'


class Customer_CreateView(generic.CreateView):
    model = Customer
    fields = ['firm','first_name', 'last_name', 'address', 'city', 'mobile_number']
    template_name = 'customers/edit.html'

    def get_success_url(self):
        return reverse_lazy('customers:customer_detail', kwargs={'pk': self.object.pk})