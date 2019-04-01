def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.content == b'Hello, world!'


def test_bye(client):
    response = client.get('/bye/')
    assert response.status_code == 200
    assert response.content == b'Bye, world!'
