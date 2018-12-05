from django import forms
from django.forms.models import inlineformset_factory
from django.forms import ModelForm

from .models import ContainerType, RateSlab


class RateSlabForm(ModelForm):
    class meta:
        model = RateSlab

    def __init__(self, *args, **kwargs):
        super(RateSlabForm, self).__init__(*args, **kwargs)


RateSlabFormSet = inlineformset_factory(
    ContainerType,
    RateSlab,
    fields=('container_type', 'rate', 'number_of_days', 'slab_number',),
    can_delete=False,
    extra=3,
    form=RateSlabForm,
)