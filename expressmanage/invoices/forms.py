from django import forms

from .models import Payment, Invoice

from expressmanage.customers.models import Customer
from expressmanage.orders.models import InwardOrder


# PAYMENT
# ------------------------------------------------------------------------------
class PaymentForm(forms.ModelForm):
    pending_amount = forms.DecimalField(max_digits=12, decimal_places=2, required=False)

    class Meta:
        model = Payment
        fields = ['customer', 'invoice', 'pending_amount', 'amount']

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['pending_amount'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = self.cleaned_data
        amount = cleaned_data['amount']
        invoice = cleaned_data['invoice']

        if amount > invoice.pending_amount:
            self.add_error('amount', 'Amount cannot be more than the invoice pending amount')
        return cleaned_data


class LotPaymentForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    lot_number = forms.ModelChoiceField(queryset=InwardOrder.objects.all())
    pending_amount = forms.DecimalField(max_digits=12, decimal_places=2, required=False)
    amount = forms.DecimalField(max_digits=12, decimal_places=2, required=False)

    def __init__(self, *args, **kwargs):
        super(LotPaymentForm, self).__init__(*args, **kwargs)
        self.fields['pending_amount'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = self.cleaned_data
        amount = cleaned_data['amount']
        pending_amount = cleaned_data['pending_amount']

        if amount > pending_amount:
            self.add_error('amount', 'Amount cannot be more than the total pending amount')
        return cleaned_data