from django.forms.models import inlineformset_factory
from django.forms import ModelForm, ValidationError

from .models import Product, ContainerType, RateSlab


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)


class ContainerTypeForm(ModelForm):
    class Meta:
        model = ContainerType
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(ContainerTypeForm, self).__init__(*args, **kwargs)


class RateSlabForm(ModelForm):
    class Meta:
        model = RateSlab
        fields = ['container_type', 'rate', 'number_of_days']

    def __init__(self, *args, **kwargs):
        super(RateSlabForm, self).__init__(*args, **kwargs)

    # def clean_rate(self):
    #     data = self.cleaned_data['rate']
    #     raise ValidationError('Rate is not good enough')
    #     return data

    # def clean(self):
    #     cleaned_data = super(RateSlabForm, self).clean()
    #     # Use either one of the below as applicable
    #     raise ValidationError('FORM VALIDATION ERROR')
    #     self.add_error('rate', 'rate is not good enough')
    #     return cleaned_data


RateSlabFormSet = inlineformset_factory(
    ContainerType,
    RateSlab,
    can_delete=False,
    extra=3,
    form=RateSlabForm,
)

RateSlabUpdateFormSet = inlineformset_factory(
    ContainerType,
    RateSlab,
    can_delete=False,
    extra=0,
    form=RateSlabForm,
)