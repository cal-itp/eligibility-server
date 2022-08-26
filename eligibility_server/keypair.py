import logging

from jwcrypto import jwk

from . import app


logger = logging.getLogger(__name__)


def _read_key_file(key_path):
    with open(key_path, "rb") as pemfile:
        key = jwk.JWK.from_pem(pemfile.read())
    return key


def get_client_public_key():
    key_path = app.app.config["CLIENT_KEY_PATH"]
    logger.info(f"Reading client key file: {key_path}")
    return _read_key_file(key_path)


def get_server_private_key():
    key_path = app.app.config["SERVER_KEY_PATH"]
    logger.info(f"Reading server key file: {key_path}")
    return _read_key_file(key_path)
