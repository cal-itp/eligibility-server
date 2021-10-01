"""
Test app routes
"""

def test_healthcheck(app, client):
  response = client.get('/healthcheck')
  assert response.status_code == 200
  assert response.data == b"Healthy"

def test_unauthorized_verify(app, client):
  response = client.get('verify')
  assert response.status_code == 403
