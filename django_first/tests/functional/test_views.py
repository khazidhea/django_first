from lxml import html

from django_first.models import Order, Product


def test_hello(db, client, data):
    client.login(username='alice', password='alice')
    response = client.get('/')
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    assert 'Hello, world!' in response
    assert 'alice' in response
    response = html.fromstring(response)
    orders = Order.objects.filter(customer__user__username='alice')
    assert len(response.cssselect('li')) == orders.count()


def test_order_view(db, client, data):
    response = client.get('/orders/1/')
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    items = response.cssselect('.list-group-item')
    assert items[0].text == 'apple 10'
    assert response.cssselect('#product') != []
    assert response.cssselect('#quantity') != []


def test_order_add_same(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': 10})
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    items = response.cssselect('.list-group-item')
    assert items[0].text == 'apple 20'


def test_order_add_new(db, client, data):
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


def test_bye(client):
    response = client.get('/bye/')
    assert response.status_code == 200
    assert response.content == b'Bye, world!'
