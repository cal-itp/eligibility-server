import pytest

from eligibility_server.app import app


@pytest.fixture
def flask():
    app.app_context().push()

    yield app


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture()
def runner():
    return app.test_cli_runner()
