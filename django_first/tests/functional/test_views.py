from lxml import html
from django.contrib.auth.models import User

from django_first.models import Order, Product, Customer


def test_login(db, client, data):
    response = client.post(
        '/login/', {'username': 'alice', 'password': 'alice'}
    )
    assert response.status_code == 302


def test_login_fail(db, client, data):
    response = client.post(
        '/login/', {'username': 'alice', 'password': 'wrongpassword'}
    )
    assert response.status_code == 401


def test_hello(db, client, data):
    client.login(username='alice', password='alice')
    response = client.get('/')
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    assert 'alice' in response
    response = html.fromstring(response)
    a = response.cssselect('a[href="/orders/"]')
    assert len(a) == 1
    products = response.cssselect('.list-group-item')
    assert len(products) == Product.objects.count()
    assert products[0].text == 'apple 10.00'


def test_order_view(db, client, data):
    response = client.get('/orders/1/')
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    items = response.cssselect('.list-group-item')
    assert items[0].text == 'apple 10'
    assert response.cssselect('#id_product') != []
    assert response.cssselect('#id_quantity') != []


def test_order_add(db, client, data):
    client.login(username='alice', password='alice')
    response = client.post('/orders/', {'location': 'Almaty'})
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    orders = response.cssselect('.list-group-item > a')
    assert len(orders) == 2
    assert orders[0].text == '1'
    assert orders[1].text == '2'


def test_order_add_item_same(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': 10})
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    items = response.cssselect('.list-group-item')
    assert items[0].text == 'apple 20'


def test_order_add_item_new(db, client, data):
    banana = Product.objects.create(name='banana', price=20)
    response = client.post(
        '/orders/1/',
        {'product': banana.id, 'quantity': 30}
    )
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    items = response.cssselect('.list-group-item')
    assert items[0].text == 'apple 10'
    assert items[1].text == 'banana 30'


def test_order_add_item_product_doesnt_exist(db, client, data):
    response = client.post('/orders/1/', {'product': 10, 'quantity': 1})
    assert response.status_code == 404
    response = response.content.decode('utf-8')
    assert response == 'Product not found'


def test_order_add_item_invalid_product_id(db, client, data):
    response = client.post('/orders/1/', {'product': 'asd', 'quantity': 1})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Validation error'


def test_order_add_item_empty_quantity(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': ''})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Validation error'


def test_order_add_item_nonint_quantity(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': 'asd'})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Validation error'


def test_order_add_item_zero_quantity(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': 0})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Validation error'


def test_order_add_item_negative_quantity(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': -10})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Validation error'


def test_bye(client):
    response = client.get('/bye/')
    assert response.status_code == 200
    assert response.content == b'Bye, world!'


def test_order_list(db, client, data):
    extra_user = User.objects.create_user(username='bob', password='alice')
    extra_customer = Customer.objects.create(name='Bob', user=extra_user)
    Order.objects.create(location='Almaty', customer=extra_customer)

    client.login(username='alice', password='alice')
    response = client.get('/orders/')
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    orders = Order.objects.filter(customer__user__username='alice')
    items = response.cssselect('.list-group-item > a')
    assert len(items) == orders.count()
    assert items[0].text == '1'
