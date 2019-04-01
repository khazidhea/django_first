def test_django(client):
    response = client.get('/')
    assert response.status_code == 404
