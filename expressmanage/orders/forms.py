# from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import InwardOrder, InOli, OutwardOrder, OutOli


class InOliResultModelForm(ModelForm):
    class meta:
        model = InOli

    def __init__(self, *args, **kwargs):
        super(InOliResultModelForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['readonly']         = True
        self.fields['container_type'].widget.attrs['readonly']  = True
        self.fields['stock'].widget.attrs['readonly']           = True


class OutOliModelForm(ModelForm):
    class meta:
        model = OutOli
        fields = ('outward_order', 'in_oli', 'quantity',)

    def clean(self):
        raise ValidationError({'quantity': ('quantity wrong')})


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
    # form=OutOliModelForm,
)