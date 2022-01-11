import pytest

from eligibility_server.app import app


@pytest.fixture
def flask():
    yield app


@pytest.fixture
def client():
    return app.test_client()
