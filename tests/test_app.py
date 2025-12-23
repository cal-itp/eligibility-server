"""
Test app
"""

import re

from eligibility_server import __version__
from eligibility_server.settings import APP_NAME
from eligibility_server.keypair import get_server_public_key


def test_appname(flask):
    assert flask.name == APP_NAME


def test_healthcheck(client):
    response = client.get("healthcheck")
    assert response.status_code == 200
    assert response.mimetype == "text/plain"
    assert response.text == "Healthy"
    assert "Strict-Transport-Security" in response.headers


def test_metadata(client):
    response = client.get("metadata")
    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert "Strict-Transport-Security" in response.headers

    data = response.json

    assert "app" in data
    assert data["app"]["version"] == __version__

    assert "db" in data
    # Validate the presence and types of the metadata fields
    assert isinstance(data["db"]["load_ts"], str)
    assert isinstance(data["db"]["file_ts"], str)
    assert isinstance(data["db"]["users"], int)
    assert isinstance(data["db"]["eligibility"], list)
    assert len(data["db"]["eligibility"]) > 0


def test_404(client):
    response = client.get("/random")

    assert response.status_code == 404
    assert response.content_type == "application/json"
    assert response.json["error"].startswith("404 Not Found: The requested URL was not found on the server.")


def test_publickey(client):
    response = client.get("publickey")
    assert response.status_code == 200
    assert response.mimetype == "text/plain"
    assert response.text == get_server_public_key().decode("utf-8")


def test_version():
    from eligibility_server import __version__

    assert __version__ is not None
    assert re.match(r"\d+\.\d+\..+", __version__)
