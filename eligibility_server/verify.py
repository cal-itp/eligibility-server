"""
Eligibility Verification route
"""

import datetime
import json
import logging
import re
import time

from flask import abort
from flask_restful import Resource, reqparse
from jwcrypto import jwe, jws, jwt

from eligibility_server import keypair
from eligibility_server.db.models import User
from eligibility_server.hash import Hash
from eligibility_server.settings import Configuration


config = Configuration()
logger = logging.getLogger(__name__)


class Verify(Resource):
    def __init__(self):
        """Initialize Verify class with a keypair and hash"""
        self.client_public_key = keypair.get_client_public_key()
        self.server_private_key = keypair.get_server_private_key()

        if config.input_hash_algo != "":
            hash = Hash(config.input_hash_algo)
            logger.debug(f"Verify initialized with hash: {hash}")
        else:
            hash = None
            logger.debug("Verify initialized without hashing")

        self.hash = hash

    def _check_headers(self):
        """Ensure correct request headers."""
        req_parser = reqparse.RequestParser()
        req_parser.add_argument(config.token_header, location="headers", required=True)
        req_parser.add_argument(config.auth_header, location="headers", required=True)
        headers = req_parser.parse_args()

        # verify auth_header's value
        if headers.get(config.auth_header) == config.auth_token:
            return headers
        else:
            return False

    def _get_token(self, headers):
        """Get the token from request headers"""
        token = headers.get(config.token_header, "").split(" ")
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
            decrypted_token = jwe.JWE(algs=[config.jwe_encryption_alg, config.jwe_cek_enc])
            decrypted_token.deserialize(token, key=self.server_private_key)
            decrypted_payload = str(decrypted_token.payload, "utf-8")
            # verify signature
            signed_token = jws.JWS()
            signed_token.deserialize(decrypted_payload, key=self.client_public_key, alg=config.jws_signing_alg)
            # return final payload
            payload = str(signed_token.payload, "utf-8")
            return json.loads(payload)
        except Exception:
            logger.warning("Get token payload failed")
            return False

    def _make_token(self, payload):
        """Wrap payload in a signed and encrypted JWT for response."""
        # sign the payload with server's private key
        header = {"typ": "JWS", "alg": config.jws_signing_alg}
        signed_token = jwt.JWT(header=header, claims=payload)
        signed_token.make_signed_token(self.server_private_key)
        signed_payload = signed_token.serialize()
        # encrypt the signed payload with client's public key
        header = {"typ": "JWE", "alg": config.jwe_encryption_alg, "enc": config.jwe_cek_enc}
        encrypted_token = jwt.JWT(header=header, claims=signed_payload)
        encrypted_token.make_encrypted_token(self.client_public_key)
        return encrypted_token.serialize()

    def _get_response(self, token_payload):
        try:
            # craft the response payload using parsed request token
            sub, name, eligibility = token_payload["sub"], token_payload["name"], list(token_payload["eligibility"])
            resp_payload = dict(
                jti=token_payload["jti"],
                iss=config.app_name,
                iat=int(datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).timestamp()),
            )
            # sub format check
            if re.match(config.sub_format_regex, sub):
                # eligibility check against db
                resp_payload["eligibility"] = self._check_user(sub, name, eligibility)
                code = 200
            else:
                resp_payload["error"] = {"sub": "invalid"}
                code = 400
            # make a response token with appropriate response code
            return self._make_token(resp_payload), code
        except (TypeError, ValueError) as ex:
            logger.error(f"Error: {ex}")
            abort(400, description="Bad request")
        except Exception as ex:
            logger.error(f"Error: {ex}")
            abort(500, description="Internal server error")

    def _check_user(self, sub, name, types):
        """
        Check if the data matches a record in the database

        @param self: self
        @param sub: sub to check for
        @param name: name of user to check for
        @param types: type of eligibility

        @return list of strings of types user is eligible for, or empty list
        """

        if len(types) < 1:
            logger.debug("List of types to check was empty.")
            return []

        if self.hash:
            sub = self.hash.hash_input(sub)
            name = self.hash.hash_input(name)

        existing_user = User.query.filter_by(sub=sub, name=name).first()
        if existing_user:
            existing_user_types = [type.name for type in existing_user.types]
        else:
            existing_user_types = []

        matching_types = set(existing_user_types) & set(types)

        if existing_user is None:
            logger.debug("Database does not contain requested user.")
            return []
        elif len(matching_types) < 1:
            logger.debug(f"User's types do not contain any of the requested types: {types}")
            return []
        else:
            return list(matching_types)

    def get(self):
        """Respond to a verification request."""
        # introduce small fake delay
        time.sleep(2)

        headers = {}

        # verify required headers and API key check
        try:
            headers = self._check_headers()
        except Exception:
            logger.error("Forbidden")
            abort(403, description="Forbidden")

        # parse inner payload from request token
        try:
            token = self._get_token(headers)
            token_payload = self._get_token_payload(token)
        except Exception:
            logger.error("Bad request")
            abort(400, description="Bad request")

        if token_payload:
            return self._get_response(token_payload)
        else:
            logger.error("Invalid token format")
            abort(400, description="Invalid token format")
