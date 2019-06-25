import pytest

from django.contrib.auth.models import User

from django_first.models import (
    Category, Attribute, AttributeValue, Product,
    Order, OrderItem, Store, StoreItem, Payment, Customer
)


@pytest.fixture
def data():
    category = Category.objects.create(name='fruits')
    attribute = Attribute.objects.create(category=category, name='size')
    size_large = AttributeValue.objects.create(
        attribute=attribute,
        value='large'
    )
    product = Product.objects.create(name='apple', price=10)
    product.attributes.add(size_large)

    store = Store.objects.create(location='Almaty')
    store_item = StoreItem.objects.create(
        store=store,
        product=product,
        quantity=100
    )
    user = User.objects.create_user(username='alice', password='alice')
    customer = Customer.objects.create(name='Alice', user=user)
    order = Order.objects.create(location='Almaty', customer=customer)
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
