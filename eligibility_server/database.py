"""
Simple hard-coded server database.
"""

import json


class Database:
    def __init__(self):
        with open("data/server.json") as f:
            data = json.load(f)
            self._users = data["users"]

    def check_user(self, key, user, types):
        """Check if the data matches a record in the database."""
        if (
            len(types) < 1
            or key not in self._users
            or self._users[key][0] != user
            or len(set(self._users[key][1]) & set(types)) < 1
        ):
            return []

        return list(set(self._users[key][1]) & set(types))
