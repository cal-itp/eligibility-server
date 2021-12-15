"""
Simple hard-coded server database.
"""

import json
import hashlib


class Database:
    def __init__(self):
        with open("data/server.json") as f:
            data = json.load(f)
            self._users = data["users"]

    def hash_input(self, input):
        """
        Return a SHA-256 hash of inputted string

        @param input: string

        @return string
        """

        return hashlib.sha256(input.encode("utf-8")).hexdigest()

    def check_user(self, key, user, types, hash_inputs=False):
        """
        Check if the data matches a record in the database, optionally, check with hashed key and user strings.

        @param self: self
        @param key: string - key to check for
        @param user: string - name of user to check for
        @param types: string - type of eligibility
        @param hash_inputs: boolean - default False, defaults to not hashing inputs

        @return array - empty array or array of strings of types user is eligible for
        """

        key_to_check = key
        user_to_check = user

        if hash_inputs:
            key_to_check = self.hash_input(key)
            user_to_check = self.hash_input(user)

        if (
            len(types) < 1
            or key_to_check not in self._users
            or self._users[key_to_check][0] != user_to_check
            or len(set(self._users[key_to_check][1]) & set(types)) < 1
        ):
            return []

        return list(set(self._users[key_to_check][1]) & set(types))
