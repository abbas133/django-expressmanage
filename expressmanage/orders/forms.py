# from django import forms
from django.forms import ModelForm, BaseInlineFormSet, ValidationError
from django.forms.models import inlineformset_factory

from .models import InwardOrder, InOli, OutwardOrder, OutOli


class InOliResultModelForm(ModelForm):
    class Meta:
        model = InOli
        fields = ('product', 'container_type', 'stock')

    def __init__(self, *args, **kwargs):
        super(InOliResultModelForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['readonly']         = True
        self.fields['container_type'].widget.attrs['readonly']  = True
        self.fields['stock'].widget.attrs['readonly']           = True


class OutOliModelForm(ModelForm):
    class Meta:
        model = OutOli
        fields = ('outward_order', 'in_oli', 'quantity',)

    def clean(self):
        cleaned_data = super(OutOliModelForm, self).clean()
        self.add_error('quantity', 'Quantity cannot be negative')
        return cleaned_data


class OutwardOrderModelForm(ModelForm):
    class Meta:
        model = OutwardOrder
        fields = ('customer', 'inward_order', 'date', 'received_by',)

    def clean(self):
        super(OutwardOrderModelForm, self).clean()
        self.add_error('date', 'The form cannot be submitted')


# InOliFormSet = inlineformset_factory(
#     InwardOrder,
#     InOli,
#     fields=('inward_order','product', 'container_type', 'quantity',),
#     can_delete=False,
# )


InOliResultFormSet = inlineformset_factory(
    InwardOrder,
    InOli,
    fields=('inward_order', 'product', 'container_type', 'stock',),
    can_delete=False,
    extra=0,
    form=InOliResultModelForm,
)


OutOliFormSet = inlineformset_factory(
    OutwardOrder,
    OutOli,
    fields=('outward_order', 'quantity',),
    can_delete=False,
    extra=2,
    form=OutOliModelForm,
)


# NEW FORMS
# ------------------------------------------------------------------------------
class BaseInOliFormSet(BaseInlineFormSet):
    # class Meta:
    #     model = InOli
    #     fields = ['inward_order','product', 'container_type', 'quantity']

    # def clean_inward_order(self):
    #     data = self.cleaned_data["inward_order"]
    #     raise ValidationError('inward_order doesnt seems right')
    #     return data

    # def clean_product(self):
    #     data = self.cleaned_data["product"]
    #     raise ValidationError('Product doesnt seems right')
    #     return data

    # def clean_container_type(self):
    #     data = self.cleaned_data["container_type"]
    #     raise ValidationError('container_type doesnt seems right')
    #     return data

    # def clean_quantity(self):
    #     data = self.cleaned_data["quantity"]
    #     raise ValidationError('quantity doesnt seems right')
    #     return data

    def clean(self):
        for form in self.forms:
            raise ValidationError('FORM VALIDATION ERROR')


InOliFormSet = inlineformset_factory(
    parent_model=InwardOrder,
    model=InOli,
    formset=BaseInOliFormSet,
    fields=('inward_order','product', 'container_type', 'quantity',),
    can_delete=False,
    extra=1,
)