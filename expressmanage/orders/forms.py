from django.forms import ModelForm, ValidationError, HiddenInput
from django.forms.models import inlineformset_factory

from .models import InwardOrder, InOli, OutwardOrder, OutOli


# INWARD ORDERS
# ------------------------------------------------------------------------------
class InwardOrderForm(ModelForm):
    class Meta:
        model = InwardOrder
        fields = ['customer', 'date', 'chamber']

    def __init__(self, *args, **kwargs):
        super(InwardOrderForm, self).__init__(*args, **kwargs)


class InOliForm(ModelForm):
    class Meta:
        model = InOli
        fields = ['inward_order','product', 'container_type', 'quantity']

    def __init__(self, *args, **kwargs):
        super(InOliForm, self).__init__(*args, **kwargs)


class InOliResultForm(ModelForm):
    class Meta:
        model = InOli
        fields = ('product', 'container_type', 'stock')

    def __init__(self, *args, **kwargs):
        super(InOliResultForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['readonly'] = True
        self.fields['container_type'].widget.attrs['readonly'] = True
        self.fields['stock'].widget.attrs['readonly'] = True


InOliFormSet = inlineformset_factory(
    InwardOrder,
    InOli,
    can_delete=False,
    extra=3,
    form=InOliForm,
)

InOliUpdateFormset = inlineformset_factory(
    InwardOrder,
    InOli,
    can_delete=False,
    extra=0,
    form=InOliForm,
)

InOliResultFormSet = inlineformset_factory(
    InwardOrder,
    InOli,
    can_delete=False,
    extra=0,
    form=InOliResultForm,
)

# OUTWARD ORDERS
# ------------------------------------------------------------------------------
class OutwardOrderForm(ModelForm):
    class Meta:
        model = OutwardOrder
        fields = ['customer', 'inward_order', 'date', 'received_by']

    def __init__(self, *args, **kwargs):
        super(OutwardOrderForm, self).__init__(*args, **kwargs)


class OutOliForm(ModelForm):
    class Meta:
        model = OutOli
        fields = ['outward_order', 'in_oli', 'quantity']

    def __init__(self, *args, **kwargs):
        super(OutOliForm, self).__init__(*args, **kwargs)
        self.fields['in_oli'].widget = HiddenInput()


OutOliFormSet = inlineformset_factory(
    OutwardOrder,
    OutOli,
    can_delete=False,
    extra=2,
    form=OutOliForm,
)