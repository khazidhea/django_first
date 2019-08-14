from django import forms
from django.forms.models import inlineformset_factory

from .models import Order, OrderItem


class OrderItemForm(forms.ModelForm):
    name = forms.CharField()
    image = forms.ImageField()
    quantity = forms.IntegerField(label='quantity', min_value=1)

    class Meta:
        model = OrderItem
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['name'] = self.instance.product.name
        print(self.instance.product.image.url)
        self.initial['image'] = self.instance.product.image.url


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, form=OrderItemForm,
    extra=0, can_delete=True
)
