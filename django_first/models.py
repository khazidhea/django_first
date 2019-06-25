from django.db import models
from django.contrib.auth.models import User

from .exceptions import StoreException, PaymentException


class Category(models.Model):
    name = models.CharField(max_length=100)


class Attribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class AttributeValue(models.Model):
    value = models.CharField(max_length=100)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    def __str__(self):
        return self.value


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    image = models.ImageField(blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.CASCADE
    )
    attributes = models.ManyToManyField(
        AttributeValue, related_name='products'
    )


class Customer(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Store(models.Model):
    location = models.CharField(max_length=100)


class StoreItem(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='store_items'
    )
    quantity = models.IntegerField()


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
        related_name='orders'
    )
    location = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )
    is_paid = models.BooleanField(default=False)

    def process(self):
        try:
            store = Store.objects.get(location=self.location)
        except Store.DoesNotExist:
            raise StoreException('Location not available')
        for item in self.items.all():
            store_item = StoreItem.objects.get(
                store=store,
                product=item.product
            )
            if item.quantity > store_item.quantity:
                raise StoreException('Not enough stock')
            store_item.quantity -= item.quantity
            store_item.save()

        if not self.is_paid:
            raise PaymentException('Not enough money')


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.IntegerField()


class Payment(models.Model):
    METHOD_CARD = 'card'
    METHOD_CASH = 'cash'
    METHOD_QIWI = 'qiwi'

    METHOD_CHOICES = (
        (METHOD_CARD, METHOD_CARD),
        (METHOD_CASH, METHOD_CASH),
        (METHOD_QIWI, METHOD_QIWI)
    )

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )
    method = models.CharField(
        max_length=10, choices=METHOD_CHOICES, default=METHOD_CARD
    )
    is_confirmed = models.BooleanField(default=False)
