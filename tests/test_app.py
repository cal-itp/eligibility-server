"""
Test app
"""

from eligibility_server.settings import APP_NAME


def test_appname(flask):
    assert flask.name == APP_NAME


def test_healthcheck(client):
    response = client.get("healthcheck")
    assert response.status_code == 200
    assert response.mimetype == "text/plain"
    assert response.text == "Healthy"


def test_404(client):
    response = client.get("/random")

    assert response.status_code == 404
    assert response.content_type == "application/json"
    assert response.json["error"].startswith("404 Not Found: The requested URL was not found on the server.")
