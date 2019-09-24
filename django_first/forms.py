from django import forms
from django.forms.models import inlineformset_factory

from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['customer']

    def clean(self):
        result = super().clean()
        print(self.errors)
        return result


class OrderItemForm(forms.ModelForm):
    name = forms.CharField(required=False)
    image = forms.ImageField(required=False)
    quantity = forms.IntegerField(min_value=1, required=False)
    price = forms.IntegerField(required=False)
    product_price = forms.IntegerField(required=False)

    class Meta:
        model = OrderItem
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].required = False
        if self.instance.pk:
            self.initial['name'] = self.instance.product.name
            self.initial['price'] = self.instance.price
            self.initial['product_price'] = self.instance.product.price
            if self.instance.product.image:
                self.initial['image'] = self.instance.product.image.url


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, form=OrderItemForm,
    extra=0, can_delete=True
)
