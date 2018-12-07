from django import forms
from django.forms import ModelForm, Textarea
from django.forms.models import inlineformset_factory, modelformset_factory

from .models import InwardOrder, InOli, OutwardOrder, OutOli


class InOliModelForm(ModelForm):
    class meta:
        model = InOli

    def __init__(self, *args, **kwargs):
        super(InOliModelForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['readonly']         = True
        self.fields['container_type'].widget.attrs['readonly']  = True
        self.fields['stock'].widget.attrs['readonly']           = True


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
    form=InOliModelForm,
)


OutOliFormSet = inlineformset_factory(
    OutwardOrder,
    OutOli,
    fields=('outward_order', 'quantity',),
    can_delete=False,
    extra=2,
)