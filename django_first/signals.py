from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem


@receiver(post_save, sender=OrderItem)
def order_item_post_save(sender, **kwargs):
    item = kwargs['instance']
    order = item.order

    duplicate = order.items.filter(
        product=item.product
    ).exclude(id=item.id).first()
    if duplicate:
        duplicate.quantity += item.quantity
        post_save.disconnect(order_item_post_save, sender=OrderItem)
        duplicate.save()
        item.delete()
        post_save.connect(order_item_post_save, sender=OrderItem)

    order.price = sum(
        (item.product.price * item.quantity for item in order.items.all())
    )
