"""
Test config settings
"""
import pytest

from eligibility_server.app import app


def test_settings():
    assert app.config["APP_NAME"] == "eligibility_server.app"
    assert app.config["HOST"] == "0.0.0.0"  # nosec
    assert app.config["AUTH_HEADER"] == "X-Server-API-Key"
    assert app.config["AUTH_TOKEN"] == "server-auth-token"
    assert app.config["TOKEN_HEADER"] == "Authorization"
    assert app.config["JWE_CEK_ENC"] == "A256CBC-HS512"
    assert app.config["JWE_ENCRYPTION_ALG"] == "RSA-OAEP"
    assert app.config["JWS_SIGNING_ALG"] == "RS256"
    assert app.config["IMPORT_FILE_FORMAT"] == "json"
    assert app.config["IMPORT_FILE_PATH"] == "data/server.json"


def test_hash_settings():
    assert app.config["INPUT_HASH_ALGO"] == "sha256"


@pytest.mark.settingstest
def test_hash_settings_env():
    assert app.config["INPUT_HASH_ALGO"] == "sha256"
    assert app.config["IMPORT_FILE_FORMAT"] == "csv"
    assert app.config["IMPORT_FILE_PATH"] == "data/server.csv"


def test_debug():
    if app.config["DEBUG_MODE"]:
        assert True


@pytest.mark.settingstest
def test_sub_format_regex_env():
    assert app.config["SUB_FORMAT_REGEX"] == "test\\"
