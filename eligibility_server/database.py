"""
Simple hard-coded server database.
"""

import ast

from . import app


class Database:
    def __init__(self, hash=False):
        """
        Initialize with database data and optionally lookup by hashing inputs

        @param hash: Hash object to lookup hashed inputs. False to lookup raw inputs.
        """

        self._hash = hash
        if hash:
            app.app.logger.debug(f"Database initialized with hash: {hash}")
        else:
            app.app.logger.debug("Database initialized without hashing")

        users = app.User.query.all()
        all_users = {}
        for user in users:
            types = ast.literal_eval(user.types)
            all_users[user.user_id] = [user.key, types]
        self._users = all_users

    def check_user(self, key: str, user: str, types: str) -> list:
        """
        Check if the data matches a record in the database

        @param self: self
        @param key: key to check for
        @param user: name of user to check for
        @param types: type of eligibility

        @return list of strings of types user is eligible for, or empty list
        """

        if self._hash:
            key = self._hash.hash_input(key)
            user = self._hash.hash_input(user)

        existing_user = app.User.query.filter_by(user_id=key, key=user).first()

        if len(types) < 1:
            app.app.logger.debug("List of types to check was empty.")
            return []
        elif existing_user is None:
            app.app.logger.debug(f"Database does not contain requested user with sub, name: {key, user}")
            return []
        elif len(set(self._users[key][1]) & set(types)) < 1:
            app.app.logger.debug(
                f"Database contains user with matching sub and name, but user's types do not contain: {types}"
            )
            return []

        return list(set(self._users[key][1]) & set(types))
