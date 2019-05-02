from django import forms

from .models import OrderItem


class OrderItemForm(forms.ModelForm):
    product = forms.IntegerField(label='product')
    quantity = forms.IntegerField(label='quantity', min_value=1)

    class Meta:
        model = OrderItem
        fields = ['quantity']
