from django.forms import ModelForm, DecimalField

from .models import Payment, Invoice


# PAYMENT
# ------------------------------------------------------------------------------
class PaymentForm(ModelForm):
    pending_amount = DecimalField(max_digits=5, decimal_places=2, required=False)

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