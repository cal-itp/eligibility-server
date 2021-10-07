import pytest

from eligibility_server.app import app as app
from eligibility_server.database import Database as Database


@pytest.fixture
def database():
    db = Database()
    return db


@pytest.fixture
def client():
    return app.test_client()
