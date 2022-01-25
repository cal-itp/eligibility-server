"""
Test config settings
"""
import pytest

from eligibility_server import settings


def test_settings():
    assert settings.APP_NAME == "eligibility_server.app"
    assert settings.HOST == "0.0.0.0"  # nosec
    assert settings.AUTH_HEADER == "X-Server-API-Key"
    assert settings.AUTH_TOKEN == "server-auth-token"
    assert settings.TOKEN_HEADER == "Authorization"
    assert settings.JWE_CEK_ENC == "A256CBC-HS512"
    assert settings.JWE_ENCRYPTION_ALG == "RSA-OAEP"
    assert settings.JWS_SIGNING_ALG == "RS256"
    assert settings.IMPORT_FILE_FORMAT == "csv"
    assert settings.IMPORT_FILE_PATH == "data/server.csv"


def test_hash_settings():
    assert settings.INPUT_HASH_ALGO == "sha256"


@pytest.mark.settingstest
def test_hash_settings_env():
    assert settings.INPUT_HASH_ALGO == "sha512"
    assert settings.IMPORT_FILE_FORMAT == "json"
    assert settings.IMPORT_FILE_PATH == "data/server.json"


def test_debug():
    if settings.DEBUG_MODE:
        assert True
