import pytest

from app import app as server
from app import Database as Database

@pytest.fixture
def app():
    yield server

@pytest.fixture
def database():
    db = Database()
    return db

@pytest.fixture
def client(app):
    return app.test_client()
