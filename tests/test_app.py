"""
Test app
"""

from eligibility_server.settings import APP_NAME


def test_appname(flask):
    assert flask.name == APP_NAME


def test_healthcheck(client):
    response = client.get("healthcheck")
    assert response.status_code == 200
    assert response.data == b"Healthy"


def test_unauthorized_verify(client):
    response = client.get("verify")
    assert response.status_code == 403
