import pytest

from eligibility_server.app import app
from eligibility_server.database import Database as Database
from eligibility_server.hash import Hash as Hash


@pytest.fixture
def flask():
    yield app


@pytest.fixture
def database():
    database = Database()
    return database


@pytest.fixture
def hash():
    hash = Hash()
    return hash


@pytest.fixture
def client():
    return app.test_client()
