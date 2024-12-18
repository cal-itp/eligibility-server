"""
Eligibility Verification route
"""

import logging
import re

from eligibility_api.server import get_token_payload, make_token, create_response_payload
from flask import abort
from flask_restful import Resource, reqparse

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

    def _get_response(self, token_payload):
        try:
            # craft the response payload using parsed request token
            sub, name, eligibility = token_payload["sub"], token_payload["name"], list(token_payload["eligibility"])
            resp_payload = create_response_payload(token_payload=token_payload, issuer=config.app_name)
            # sub format check
            if re.match(config.sub_format_regex, sub):
                # eligibility check against db
                resp_payload["eligibility"] = self._check_user(sub, name, eligibility)
                code = 200
            else:
                resp_payload["error"] = {"sub": "invalid"}
                code = 400
            # make a response token, and return with appropriate response code
            response_token = make_token(
                payload=resp_payload,
                jws_signing_alg=config.jws_signing_alg,
                server_private_key=self.server_private_key,
                jwe_encryption_alg=config.jwe_encryption_alg,
                jwe_cek_enc=config.jwe_cek_enc,
                client_public_key=self.client_public_key,
            )
            return response_token, code
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
        else:
            logger.debug(f"Types to check: {types}")

        if self.hash:
            sub = self.hash.hash_input(sub)
            name = self.hash.hash_input(name)

            logger.debug(f"Hashed sub, name: {sub},{name}")

        existing_user = User.query.filter_by(sub=sub, name=name).first()
        if existing_user:
            existing_user_types = [type.name for type in existing_user.types]
            logger.debug(f"Existing types on user: {existing_user_types}")
        else:
            existing_user_types = []

        matching_types = set(existing_user_types) & set(types)
        logger.debug(f"Matching types: {matching_types}")

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
            token_payload = get_token_payload(
                token=token,
                jwe_encryption_alg=config.jwe_encryption_alg,
                jwe_cek_enc=config.jwe_cek_enc,
                server_private_key=self.server_private_key,
                jws_signing_alg=config.jws_signing_alg,
                client_public_key=self.client_public_key,
            )
        except Exception:
            logger.error("Bad request")
            abort(400, description="Bad request")

        if token_payload:
            return self._get_response(token_payload)
        else:
            logger.error("Invalid token format")
            abort(400, description="Invalid token format")
