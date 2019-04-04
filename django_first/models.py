from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )


class Store(models.Model):
    location = models.CharField(max_length=100, blank=True)


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
    location = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )
    is_paid = models.BooleanField(default=False)

    def process(self):
        store = Store.objects.get(location=self.location)
        for item in self.items.all():
            store_item = StoreItem.objects.get(
                store=store,
                product=item.product
            )
            store_item.quantity -= item.quantity
            store_item.save()

        self.price = sum(
            (item.product.price * item.quantity for item in self.items.all())
        )
        self.is_paid = True
        self.save()


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
