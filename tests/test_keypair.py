import builtins

import pytest
import requests
from jwcrypto import jwk

from eligibility_server import keypair
from eligibility_server.keypair import _read_key_file


@pytest.fixture
def sample_key_path_local():
    return "./keys/server.pub"


@pytest.fixture
def sample_key_path_remote():
    return "https://raw.githubusercontent.com/cal-itp/eligibility-server/dev/keys/server.pub"


@pytest.fixture
def reset_cache():
    keypair._CACHE = {}


@pytest.fixture
def spy_open(mocker):
    return mocker.spy(builtins, "open")


@pytest.fixture
def spy_requests_get(mocker):
    return mocker.spy(requests, "get")


@pytest.mark.usefixtures("reset_cache")
def test_read_key_file_local(mocker, sample_key_path_local, spy_open):
    key = jwk.JWK.from_pem(_read_key_file(sample_key_path_local))

    # check that there was a call to open the default path
    assert mocker.call(sample_key_path_local, "rb") in spy_open.call_args_list
    assert key
    assert key.key_id
    assert key.key_type == "RSA"


@pytest.mark.usefixtures("reset_cache")
def test_read_key_file_remote(sample_key_path_remote, spy_open, spy_requests_get):
    key = jwk.JWK.from_pem(_read_key_file(sample_key_path_remote))

    # check that there was no call to open
    assert spy_open.call_count == 0
    # check that we made a get request
    spy_requests_get.assert_called_with(sample_key_path_remote)
    assert key
    assert key.key_id
    assert key.key_type == "RSA"


@pytest.mark.usefixtures("reset_cache")
def test_keypair_cache(sample_key_path_local, sample_key_path_remote):
    assert keypair._CACHE == {}

    key = _read_key_file(sample_key_path_local)
    assert sample_key_path_local in keypair._CACHE
    assert key in keypair._CACHE.values()
    assert sample_key_path_remote not in keypair._CACHE

    key = _read_key_file(sample_key_path_remote)
    assert sample_key_path_remote in keypair._CACHE
    assert key in keypair._CACHE.values()
    assert sample_key_path_local in keypair._CACHE
