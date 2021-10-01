import pytest

from app import app as server

@pytest.fixture
def app():
    yield server

@pytest.fixture
def client(app):
    return app.test_client()
