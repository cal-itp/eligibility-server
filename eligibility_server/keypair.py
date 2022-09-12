import logging

from jwcrypto import jwk
import requests

from eligibility_server.settings import Configuration


config = Configuration()
logger = logging.getLogger(__name__)


_CACHE = {}


def _read_key_file(key_path):
    if key_path in _CACHE:
        return _CACHE[key_path]

    if key_path.startswith("http"):
        data = requests.get(key_path).text
        key = jwk.JWK.from_pem(data.encode("utf8"))
    else:
        with open(key_path, "rb") as pemfile:
            key = jwk.JWK.from_pem(pemfile.read())

    _CACHE[key_path] = key

    return key


def get_client_public_key():
    key_path = config.client_key_path
    logger.info(f"Reading client key file: {key_path}")
    return _read_key_file(key_path)


def get_server_private_key():
    key_path = config.server_private_key_path
    logger.info(f"Reading server private key file: {key_path}")
    return _read_key_file(key_path)


def get_server_public_key():
    key_path = config.server_public_key_path
    logger.info(f"Reading server public key file: {key_path}")
    return _read_key_file(key_path)
