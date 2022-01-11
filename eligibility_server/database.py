"""
Simple hard-coded server database.
"""

import json


class Database:
    def __init__(self, hash: bool):
        """
        Initialize database with server data and initialize hash

        @param hash: Boolean, whether to hash inputs or not
        """

        self._hash = hash or False

        with open("data/server.json") as f:
            data = json.load(f)
            self._users = data["users"]

    def check_user(self, key: str, user: str, types: str) -> list:
        """
        Check if the data matches a record in the database, optionally, check with hashed key and user strings.

        @param self: self
        @param key: key to check for
        @param user: name of user to check for
        @param types: type of eligibility

        @return list of strings of types user is eligible for, or empty list
        """

        if self._hash:
            key_to_check = hash.hash_input(key)
            user_to_check = hash.hash_input(user)
        else:
            key_to_check = key
            user_to_check = user

        if (
            len(types) < 1
            or key_to_check not in self._users
            or self._users[key_to_check][0] != user_to_check
            or len(set(self._users[key_to_check][1]) & set(types)) < 1
        ):
            return []

        return list(set(self._users[key_to_check][1]) & set(types))
