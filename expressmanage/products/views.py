from django.views import generic
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Product, ContainerType, RateSlab
from .forms import RateSlabFormSet


# PRODUCT
# ------------------------------------------------------------------------------
class Product_IndexView(LoginRequiredMixin, generic.ListView):
    raise_exception = True
    permission_required = ('products.view_product')

    template_name = 'products/index.html'

    def get_queryset(self):
        return Product.objects.all()


class Product_DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    raise_exception = True
    permission_required = ('products.view_product')

    model = Product
    template_name = 'products/detail.html'


class Product_CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    raise_exception = True
    permission_required = ('products.add_product')

    model = Product
    fields = ['name']
    template_name = 'products/edit.html'

    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'pk': self.object.pk})


class Product_UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    raise_exception = True
    permission_required = ('products.change_product')

    model = Product
    fields = ['name']
    template_name = 'products/edit.html'

    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'pk': self.object.pk})


class Product_DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    raise_exception = True
    permission_required = ('products.delete_product')

    model = Product
    template_name = 'products/delete.html'
    success_url = reverse_lazy('products:product_index')


# CONTAINER TYPE
# ------------------------------------------------------------------------------
class ContainerType_IndexView(LoginRequiredMixin, generic.ListView):
    raise_exception = True
    permission_required = ('products.view_containertype')

    template_name = 'containers/index.html'

    def get_queryset(self):
        return ContainerType.objects.all()


class ContainerType_DetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    raise_exception = True
    permission_required = ('products.view_containertype')

    model = ContainerType
    template_name = 'containers/detail.html'


class ContainerType_CreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    raise_exception = True
    permission_required = ('products.add_containertype')

    model = ContainerType
    fields = ['name', 'description']
    template_name = 'containers/edit.html'

    def get_context_data(self, **kwargs):
        context = super(ContainerType_CreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['rate_slabs'] = RateSlabFormSet(self.request.POST)
        else:
            context['rate_slabs'] = RateSlabFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        rate_slabs = context['rate_slabs']

        with transaction.atomic():
            self.object = form.save()

            if rate_slabs.is_valid():
                rate_slabs.instance = self.object
                rate_slabs.save()
        return super(ContainerType_CreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('products:container_detail', kwargs={'pk': self.object.pk})


class ContainerType_UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    raise_exception = True
    permission_required = ('products.change_containertype')

    model = ContainerType
    fields = ['name', 'description']
    template_name = 'containers/edit.html'

    def get_context_data(self, **kwargs):
        context = super(ContainerType_UpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['rate_slabs'] = RateSlabFormSet(self.request.POST, instance=self.object)
            context['rate_slabs'].full_clean()
        else:
            context['rate_slabs'] = RateSlabFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        rate_slabs = context['rate_slabs']

        with transaction.atomic():
            self.object = form.save()

            if rate_slabs.is_valid():
                rate_slabs.instance = self.object
                rate_slabs.save()
        return super(ContainerType_UpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('products:container_detail', kwargs={'pk': self.object.pk})


class ContainerType_DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    raise_exception = True
    permission_required = ('products.delete_containertype')

    model = ContainerType
    template_name = 'containers/delete.html'
    success_url = reverse_lazy('products:container_index')