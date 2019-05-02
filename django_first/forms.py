from django import forms


class OrderItemForm(forms.Form):
    product = forms.IntegerField(label='product')
    quantity = forms.IntegerField(label='quantity', min_value=1)
