import builtins
from os.path import exists
from tempfile import NamedTemporaryFile

import pytest
import requests

from eligibility_server import keypair
from eligibility_server.keypair import get_client_public_key, get_server_private_key


@pytest.fixture
def open_spy(mocker):
    return mocker.spy(builtins, "open")


@pytest.fixture
def reset_cache():
    keypair._CACHE = {}


@pytest.mark.parametrize("key_path_setting", ["CLIENT_KEY_PATH", "SERVER_PRIVATE_KEY_PATH"])
@pytest.mark.usefixtures("reset_cache")
def test_get_keypair_default(flask, mocker, open_spy, key_path_setting):
    assert key_path_setting in flask.config
    default_path = flask.config[key_path_setting]
    assert exists(default_path)

    if "CLIENT" in key_path_setting:
        key = get_client_public_key()
    elif "PRIVATE" in key_path_setting:
        key = get_server_private_key()

    # check that there was a call to open the default path
    assert mocker.call(default_path, "rb") in open_spy.call_args_list
    assert key
    assert key.key_id
    assert key.key_type == "RSA"


@pytest.mark.usefixtures("reset_cache")
@pytest.mark.parametrize("key_path_setting", ["CLIENT_KEY_PATH", "SERVER_PRIVATE_KEY_PATH"])
def test_get_keypair_custom(flask, mocker, open_spy, key_path_setting):
    default_path = flask.config[key_path_setting]

    # copy the sample key into tempfile
    with NamedTemporaryFile("wb") as tf:
        assert tf.name != default_path
        assert tf.name not in flask.config

        with open(default_path, "rb") as df:
            tf.write(df.read())
            tf.seek(0)

        mocked_config = {key_path_setting: tf.name}
        mocker.patch.dict("eligibility_server.keypair.app.app.config", mocked_config)

        if "CLIENT" in key_path_setting:
            key = get_client_public_key()
        elif "PRIVATE" in key_path_setting:
            key = get_server_private_key()

        # check that there was a call to open the tempfile path
        assert mocker.call(tf.name, "rb") in open_spy.call_args_list
        assert key
        assert key.key_id
        assert key.key_type == "RSA"


@pytest.mark.usefixtures("reset_cache")
@pytest.mark.parametrize(
    "key_path_setting,key_path",
    [
        ("CLIENT_KEY_PATH", "https://raw.githubusercontent.com/cal-itp/eligibility-server/main/keys/client.pub"),
        ("SERVER_PRIVATE_KEY_PATH", "https://raw.githubusercontent.com/cal-itp/eligibility-server/main/keys/server.key"),
    ],
)
def test_get_keypair_remote(mocker, open_spy, key_path_setting, key_path):
    mocked_config = {key_path_setting: key_path}
    mocker.patch.dict("eligibility_server.keypair.app.app.config", mocked_config)
    requests_spy = mocker.spy(requests, "get")

    if "CLIENT" in key_path_setting:
        key = get_client_public_key()
    elif "PRIVATE" in key_path_setting:
        key = get_server_private_key()

    # check that there was no call to open
    assert open_spy.call_count == 0
    # check that we made a get request
    requests_spy.assert_called_with(key_path)
    assert key
    assert key.key_id
    assert key.key_type == "RSA"


@pytest.mark.usefixtures("reset_cache")
@pytest.mark.parametrize("key_path_setting", ["CLIENT_KEY_PATH", "SERVER_PRIVATE_KEY_PATH"])
def test_keypair_cache(key_path_setting):
    assert keypair._CACHE == {}

    if "CLIENT" in key_path_setting:
        key = get_client_public_key()
    elif "PRIVATE" in key_path_setting:
        key = get_server_private_key()

    assert key in keypair._CACHE.values()
