from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Product, ContainerType, RateSlab
from .forms import ProductForm, ContainerTypeForm, RateSlabFormSet, RateSlabUpdateFormSet


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
    form_class = ProductForm
    template_name = 'products/edit.html'

    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'pk': self.object.pk})


class Product_UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    raise_exception = True
    permission_required = ('products.change_product')

    model = Product
    form_class = ProductForm
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
    template_name = 'containers/edit.html'
    form_class = ContainerTypeForm
    object = None

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        rate_slab_formset = RateSlabFormSet()

        return self.render_to_response(
            self.get_context_data(form=form, rate_slab_formset=rate_slab_formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        rate_slab_formset = RateSlabFormSet(self.request.POST)

        if form.is_valid() and rate_slab_formset.is_valid():
            return self.form_valid(form, rate_slab_formset)
        else:
            return self.form_invalid(form, rate_slab_formset)

    def form_valid(self, form, rate_slab_formset):
        self.object = form.save(commit=False)
        self.object.save()

        rate_slabs = rate_slab_formset.save(commit=False)
        for rs in rate_slabs:
            rs.container_type = self.object
            rs.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, rate_slab_formset):
        return self.render_to_response(
            self.get_context_data(form=form, rate_slab_formset=rate_slab_formset)
        )

    def get_success_url(self):
        return reverse_lazy('products:container_detail', kwargs={'pk': self.object.pk})


class ContainerType_UpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    raise_exception = True
    permission_required = ('products.change_containertype')

    model = ContainerType
    template_name = 'containers/edit.html'
    form_class = ContainerTypeForm
    object = None

    def get_object(self, queryset=None):
        self.object = super(ContainerType_UpdateView, self).get_object()
        return self.object

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        rate_slab_formset = RateSlabUpdateFormSet(instance=self.object)

        return self.render_to_response(
            self.get_context_data(form=ContainerTypeForm(instance=self.object), rate_slab_formset=rate_slab_formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ContainerTypeForm(data=self.request.POST, instance=self.object)
        rate_slab_formset = RateSlabUpdateFormSet(data=self.request.POST, instance=self.object)

        if form.is_valid() and rate_slab_formset.is_valid():
            return self.form_valid(form, rate_slab_formset)
        else:
            return self.form_invalid(form, rate_slab_formset)

    def form_valid(self, form, rate_slab_formset):
        self.object = form.save()
        rate_slabs = rate_slab_formset.save(commit=False)

        for rs in rate_slabs:
            rs.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, rate_slab_formset):
        return self.render_to_response(
            self.get_context_data(form=form, rate_slab_formset=rate_slab_formset)
        )

    def get_success_url(self):
        return reverse_lazy('products:container_detail', kwargs={'pk': self.object.pk})


class ContainerType_DeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    raise_exception = True
    permission_required = ('products.delete_containertype')

    model = ContainerType
    template_name = 'containers/delete.html'
    success_url = reverse_lazy('products:container_index')