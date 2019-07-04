import pytest

from django.contrib.auth.models import User

from django_first.models import (
    Category, Attribute, AttributeValue, Product,
    Order, OrderItem, Store, StoreItem, Payment, Customer
)


@pytest.fixture
def data():
    category = Category.objects.create(name='fruits')
    size = Attribute.objects.create(category=category, name='size')
    color = Attribute.objects.create(category=category, name='color')

    size_large = AttributeValue.objects.create(attribute=size, value='large')
    size_medium = AttributeValue.objects.create(attribute=size, value='medium')
    size_small = AttributeValue.objects.create(attribute=size, value='small')

    color_green = AttributeValue.objects.create(attribute=color, value='green')
    color_yellow = AttributeValue.objects.create(
        attribute=color, value='yellow'
    )

    large_green_apple = Product.objects.create(name='apple', price=10)
    large_green_apple.attributes.set([size_large, color_green])
    medium_green_apple = Product.objects.create(name='apple', price=7)
    medium_green_apple.attributes.set([size_medium, color_green])
    small_green_apple = Product.objects.create(name='apple', price=5)
    small_green_apple.attributes.set([size_small, color_green])

    large_yellow_banana = Product.objects.create(name='banana', price=10)
    large_yellow_banana.attributes.set([size_large, color_yellow])

    store = Store.objects.create(location='Almaty')
    store_item = StoreItem.objects.create(
        store=store,
        product=large_green_apple,
        quantity=100
    )
    user = User.objects.create_user(username='alice', password='alice')
    customer = Customer.objects.create(name='Alice', user=user)
    order = Order.objects.create(location='Almaty', customer=customer)
    order_item = OrderItem.objects.create(
        order=order,
        product=large_green_apple,
        quantity=10
    )
    payment = Payment.objects.create(
        order=order,
        amount=1000,
        is_confirmed=True
    )
    return large_green_apple, store, store_item, order, order_item, payment
