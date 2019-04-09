import pytest

from django_first.models import (
    Order, OrderItem, Product, Store, StoreItem, Payment, Customer
)
from django_first.exceptions import StoreException, PaymentException


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
    customer = Customer.objects.create(
        name='Alice'
    )
    order = Order.objects.create(
        location='Almaty',
        customer=customer
    )
    order_item = OrderItem.objects.create(
        order=order,
        product=product,
        quantity=10
    )
    payment = Payment.objects.create(
        order=order,
        amount=1000,
        is_confirmed=True
    )
    return product, store, store_item, order, order_item, payment


def test_order_process_ok(db, data):
    product, store, store_item, order, order_item, payment = data
    order.process()
    store_item.refresh_from_db()
    assert order.price == 100
    assert order.is_paid is True
    assert store_item.quantity == 90
    assert order.customer.name == 'Alice'


def test_order_process_ok_mulitple_payments(db, data):
    product, store, store_item, order, order_item, payment = data
    payment.amount = 50
    payment.save()
    Payment.objects.create(
        order=order,
        amount=50,
        is_confirmed=True
    )
    order.process()
    store_item.refresh_from_db()
    assert order.price == 100
    assert order.is_paid is True
    assert store_item.quantity == 90


def test_order_process_fail_not_enough_stock(db, data):
    product, store, store_item, order, order_item, payment = data
    order_item.quantity = 200
    order_item.save()
    with pytest.raises(StoreException) as e:
        order.process()
    assert str(e.value) == 'Not enough stock'


def test_order_process_fail_not_enough_money(db, data):
    product, store, store_item, order, order_item, payment = data
    payment.amount = 10
    payment.save()
    with pytest.raises(PaymentException) as e:
        order.process()
    assert str(e.value) == 'Not enough money'


def test_order_process_fail_payment_not_confirmed(db, data):
    product, store, store_item, order, order_item, payment = data
    payment.is_confirmed = False
    payment.save()
    with pytest.raises(PaymentException) as e:
        order.process()
    assert str(e.value) == 'Not enough money'


def test_order_process_fail_location_not_available(db, data):
    product, store, store_item, order, order_item, payment = data
    order.location = 'Astana'
    order.save()
    with pytest.raises(StoreException) as e:
        order.process()
    assert str(e.value) == 'Location not available'
