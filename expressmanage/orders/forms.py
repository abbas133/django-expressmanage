from django.forms import ModelForm, ValidationError, HiddenInput
from django.forms.models import inlineformset_factory

from .models import InwardOrder, InOli, OutwardOrder, OutOli
from .helpers import get_oli_applicable_rate

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


class InOliUpdateForm(ModelForm):
    class Meta:
        model = InOli
        fields = ['product', 'container_type', 'quantity', 'stock']

    def __init__(self, *args, **kwargs):
        super(InOliUpdateForm, self).__init__(*args, **kwargs)


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
    form=InOliUpdateForm,
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


class OutwardOrderUpdateForm(ModelForm):
    class Meta:
        model = OutwardOrder
        fields = ['customer', 'inward_order', 'date', 'received_by']

    def __init__(self, *args, **kwargs):
        super(OutwardOrderUpdateForm, self).__init__(*args, **kwargs)
        self.fields['customer'].widget.attrs['readonly'] = True
        self.fields['inward_order'].widget.attrs['readonly'] = True


class OutOliForm(ModelForm):
    class Meta:
        model = OutOli
        fields = ['outward_order', 'in_oli', 'quantity']

    def __init__(self, *args, **kwargs):
        super(OutOliForm, self).__init__(*args, **kwargs)
        self.fields['in_oli'].widget = HiddenInput()

    def clean(self):
        cleaned_data = super(OutOliForm, self).clean()
        quantity = cleaned_data['quantity']
        stock = cleaned_data['in_oli'].stock

        try:
            oli = self.save(commit=False)
            oli.in_oli = cleaned_data['in_oli']
            oli.outward_order = cleaned_data['outward_order']

            get_oli_applicable_rate(oli)

        except Exception as e:
            self.add_error('quantity', 'Rate slab not configured for the number of days this item has elaped. Please re-configure the rate slab and try again')


        if quantity > stock:
            self.add_error('quantity', 'Qauntity cannot be more than available stock')
        return cleaned_data


OutOliFormSet = inlineformset_factory(
    OutwardOrder,
    OutOli,
    can_delete=False,
    extra=2,
    form=OutOliForm,
)

OutOliResultFormSet = inlineformset_factory(
    OutwardOrder,
    OutOli,
    can_delete=False,
    extra=0,
    form=OutOliForm,
)