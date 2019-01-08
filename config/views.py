from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.db.models import Sum

from expressmanage.customers.models import Customer
from expressmanage.invoices.models import Payment
from expressmanage.orders.models import InwardOrder, OutwardOrder


class Dashboard_DetailView(LoginRequiredMixin, TemplateView):
    raise_exception = True
    template_name = 'pages/home.html'

    def get(self, request, *args, **kwargs):
        total_customers = Dashboard_DetailView.get_total_customers()
        todays_collection = Dashboard_DetailView.get_todays_collection()
        todays_inward_orders = Dashboard_DetailView.get_todays_inward_orders()
        todays_outward_orders = Dashboard_DetailView.get_todays_outward_orders()

        return self.render_to_response(
            self.get_context_data(
                total_customers=total_customers, 
                todays_collection=todays_collection, 
                todays_inward_orders=todays_inward_orders, 
                todays_outward_orders=todays_outward_orders
            )
        )

    def get_total_customers():
        return Customer.objects.all().count()

    def get_todays_collection():
        return Payment.objects.filter(created__date=timezone.now().date()).aggregate(Sum('amount'))['amount__sum']

    def get_todays_inward_orders():
        return InwardOrder.objects.filter(created__date=timezone.now().date()).count()

    def get_todays_outward_orders():
        return OutwardOrder.objects.filter(created__date=timezone.now().date()).count()