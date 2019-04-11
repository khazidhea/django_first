from lxml import html

from django_first.models import Order


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


def test_bye(client):
    response = client.get('/bye/')
    assert response.status_code == 200
    assert response.content == b'Bye, world!'
