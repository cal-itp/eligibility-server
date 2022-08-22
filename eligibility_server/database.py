"""
Simple hard-coded server database.
"""

import ast

from . import app
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, hash=False):
        """
        Initialize with database data and optionally lookup by hashing inputs

        @param hash: Hash object to lookup hashed inputs. False to lookup raw inputs.
        """

        self._hash = hash
        if hash:
            logger.debug(f"Database initialized with hash: {hash}")
        else:
            logger.debug("Database initialized without hashing")

    def check_user(self, sub: str, name: str, types: str) -> list:
        """
        Check if the data matches a record in the database

        @param self: self
        @param sub: sub to check for
        @param name: name of user to check for
        @param types: type of eligibility

        @return list of strings of types user is eligible for, or empty list
        """

        if self._hash:
            sub = self._hash.hash_input(sub)
            name = self._hash.hash_input(name)

        existing_user = app.User.query.filter_by(sub=sub, name=name).first()
        if existing_user:
            existing_user_types = ast.literal_eval(existing_user.types)
        else:
            existing_user_types = None

        if len(types) < 1:
            logger.debug("List of types to check was empty.")
            return []
        elif existing_user is None:
            logger.debug("Database does not contain requested user.")
            return []
        elif len(set(existing_user_types) & set(types)) < 1:
            logger.debug(f"Database contains user with matching sub and name, but user's types do not contain: {types}")
            return []
        else:
            matching_types = set(existing_user_types) & set(types)
            return list(matching_types)
