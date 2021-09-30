import pytest

from app import app as flask_app

@pytest.fixture
def app():
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
