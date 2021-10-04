def test_healthcheck(app, client):
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.data == b"Healthy"
