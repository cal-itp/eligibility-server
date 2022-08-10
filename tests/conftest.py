import pytest

from eligibility_server.app import app


@pytest.fixture
def flask():
    yield app


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def mock_config(mocker):
    def get_mocked_config(custom_config_dict):
        config = {k: v for (k, v) in app.config.items()}
        config.update(custom_config_dict)

        mock = mocker.MagicMock()
        mock.__getitem__.side_effect = config.__getitem__
        return mock

    return get_mocked_config
