# from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

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
        # self.add_error('date', 'The form cannot be submitted')


InOliFormSet = inlineformset_factory(
    InwardOrder,
    InOli,
    fields=('inward_order','product', 'container_type', 'quantity',),
    can_delete=False,
)


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