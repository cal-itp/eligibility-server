"""
Test config settings
"""

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


def test_debug():
    if settings.DEBUG_MODE:
        assert settings.DEBUG_MODE
    else:
        assert False
