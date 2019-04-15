from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem


@receiver(post_save, sender=OrderItem)
def order_item_post_save(sender, **kwargs):
    item = kwargs['instance']
    order = item.order
    order.price = sum(
        (item.product.price * item.quantity for item in order.items.all())
    )
