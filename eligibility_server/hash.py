"""
Hashing tool.
"""

import hashlib


class Hash:
    def __init__(self, hash_type: str):
        """
        Initialize variable (hash_type) from settings.py variables
        """

        algorithms_available = hashlib.algorithms_available

        if hash_type in algorithms_available:
            self._hash_type = hash_type
        else:
            raise ValueError("Invalid hash_type, must be one of: " + (" ").join(algorithms_available))

    def hash_input(self, input: str) -> str:
        """
        Return a hash of inputted string, encoded in UTF-8, and in hexdigest format
        """

        return hashlib.new(self._hash_type, input.encode("utf-8")).hexdigest()
