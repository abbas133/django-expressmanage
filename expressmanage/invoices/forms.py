from django.forms import ModelForm

from .models import Payment

class PaymentForm(ModelForm):
    class Meta:
        model = Payment

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)