"""
Eligibility Verification route
"""

import datetime
import json
import re
import time

from flask import abort
from flask_restful import Resource, reqparse
from jwcrypto import jwe, jwk, jws, jwt

from . import app
from .database import Database
from .hash import Hash
import logging


logger = logging.getLogger(__name__)

with open("./keys/server.key", "rb") as pemfile:
    server_private_key = jwk.JWK.from_pem(pemfile.read())
with open("./keys/client.pub", "rb") as pemfile:
    client_public_key = jwk.JWK.from_pem(pemfile.read())


class Verify(Resource):
    def __init__(self):
        """Initialize Verify class with a Database and optionally a Hash"""
        if app.app.config["INPUT_HASH_ALGO"] != "":
            hash = Hash(app.app.config["INPUT_HASH_ALGO"])
            self._db = Database(hash=hash)
        else:
            self._db = Database()

    def _check_headers(self):
        """Ensure correct request headers."""
        req_parser = reqparse.RequestParser()
        req_parser.add_argument(app.app.config["TOKEN_HEADER"], location="headers", required=True)
        req_parser.add_argument(app.app.config["AUTH_HEADER"], location="headers", required=True)
        headers = req_parser.parse_args()
        # verify auth_header's value
        if headers.get(app.app.config["AUTH_HEADER"]) == app.app.config["AUTH_TOKEN"]:
            return headers
        else:
            return False

    def _get_token(self, headers):
        """Get the token from request headers"""
        token = headers.get(app.app.config["TOKEN_HEADER"], "").split(" ")
        if len(token) == 2:
            return token[1]
        elif len(token) == 1:
            return token[0]
        else:
            logger.warning("Invalid token format")
            raise ValueError("Invalid token format")

    def _get_token_payload(self, token):
        """Decode a token (JWE(JWS))."""
        try:
            # decrypt
            decrypted_token = jwe.JWE(algs=[app.app.config["JWE_ENCRYPTION_ALG"], app.app.config["JWE_CEK_ENC"]])
            decrypted_token.deserialize(token, key=server_private_key)
            decrypted_payload = str(decrypted_token.payload, "utf-8")
            # verify signature
            signed_token = jws.JWS()
            signed_token.deserialize(decrypted_payload, key=client_public_key, alg=app.app.config["JWS_SIGNING_ALG"])
            # return final payload
            payload = str(signed_token.payload, "utf-8")
            return json.loads(payload)
        except Exception:
            logger.warning("Get token payload failed")
            return False

    def _make_token(self, payload):
        """Wrap payload in a signed and encrypted JWT for response."""
        # sign the payload with server's private key
        header = {"typ": "JWS", "alg": app.app.config["JWS_SIGNING_ALG"]}
        signed_token = jwt.JWT(header=header, claims=payload)
        signed_token.make_signed_token(server_private_key)
        signed_payload = signed_token.serialize()
        # encrypt the signed payload with client's public key
        header = {"typ": "JWE", "alg": app.app.config["JWE_ENCRYPTION_ALG"], "enc": app.app.config["JWE_CEK_ENC"]}
        encrypted_token = jwt.JWT(header=header, claims=signed_payload)
        encrypted_token.make_encrypted_token(client_public_key)
        return encrypted_token.serialize()

    def _get_response(self, token_payload):
        try:
            # craft the response payload using parsed request token
            sub, name, eligibility = token_payload["sub"], token_payload["name"], list(token_payload["eligibility"])
            resp_payload = dict(
                jti=token_payload["jti"],
                iss=app.app.config["APP_NAME"],
                iat=int(datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).timestamp()),
            )
            # sub format check
            if re.match(app.app.config["SUB_FORMAT_REGEX"], sub):
                # eligibility check against db
                resp_payload["eligibility"] = self._db.check_user(sub, name, eligibility)
                code = 200
            else:
                resp_payload["error"] = {"sub": "invalid"}
                code = 400
            # make a response token with appropriate response code
            return self._make_token(resp_payload), code
        except Exception as ex:
            logger.warning(f"Error: {ex}")
            if ex.__doc__ == "Inappropriate argument type.":
                abort(400, description="Bad request")
            else:
                abort(500, description="Internal server error")

    def get(self):
        """Respond to a verification request."""
        # introduce small fake delay
        time.sleep(2)

        headers = {}

        # verify required headers and API key check
        try:
            headers = self._check_headers()
        except Exception:
            logger.warning("Unauthorized")
            abort(403, description="Unauthorized")

        # parse inner payload from request token
        try:
            token = self._get_token(headers)
            token_payload = self._get_token_payload(token)
        except Exception as ex:
            logger.warning(f"Bad request: {ex}")
            return str(ex), 400

        if token_payload:
            return self._get_response(token_payload)
        else:
            logger.warning("Invalid token format")
            return "Invalid token format", 400
