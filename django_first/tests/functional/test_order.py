import pytest

from django_first.models import Order, OrderItem, Product, Store, StoreItem


@pytest.fixture
def data():
    product = Product.objects.create(
        name='apple',
        price=10
    )
    store = Store.objects.create(
        location='Almaty',
    )
    store_item = StoreItem.objects.create(
        store=store,
        product=product,
        quantity=100
    )
    order = Order.objects.create(
        location='Almaty'
    )
    order_item = OrderItem.objects.create(
        order=order,
        product=product,
        quantity=10
    )
    return product, store, store_item, order, order_item


def test_order_process_ok(db, data):
    product, store, store_item, order, order_item = data
    order.process()
    store_item.refresh_from_db()
    assert order.price == 100
    assert order.is_paid is True
    assert store_item.quantity == 90


def test_order_process_fail_not_enough(db, data):
    product, store, store_item, order, order_item = data
    order_item.quantity = 200
    order_item.save()
    with pytest.raises(Exception) as e:
        order.process()
    assert str(e.value) == 'Not enough stock'
