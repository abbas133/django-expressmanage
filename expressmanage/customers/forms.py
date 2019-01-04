from django.forms import ModelForm, ValidationError

from .models import Customer


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['firm','name', 'address', 'city', 'mobile_number']

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)