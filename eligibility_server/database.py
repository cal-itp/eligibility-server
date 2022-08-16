"""
Simple hard-coded server database.
"""

from . import app


class Database:
    def __init__(self, hash=False):
        """
        Initialize with database data and optionally lookup by hashing inputs

        @param hash: Hash object to lookup hashed inputs. False to lookup raw inputs.
        """

        self._hash = hash

        users = app.User.query.all()
        all_users = {}
        for user in users:
            types = [type.name for type in user.types]
            all_users[user.user_id] = [user.user_name, types]
        self._users = all_users

    def check_user(self, user_id: str, user_name: str, types: str) -> list:
        """
        Check if the data matches a record in the database

        @param self: self
        @param key: key to check for
        @param user: name of user to check for
        @param types: type of eligibility

        @return list of strings of types user is eligible for, or empty list
        """

        if self._hash:
            user_id = self._hash.hash_input(user_id)
            user_name = self._hash.hash_input(user_name)

        if (
            len(types) < 1
            or user_id not in self._users
            or self._users[user_id][0] != user_name
            or len(set(self._users[user_id][1]) & set(types)) < 1
        ):
            return []

        return list(set(self._users[user_id][1]) & set(types))
