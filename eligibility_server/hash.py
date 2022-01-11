"""
Hashing tool.
"""

import hashlib


class Hash:
    def __init__(self, hash_type="sha256"):
        """
        Initialize variable (hash_type) from settings.py variables
        """

        self._hash_type = hash_type or "sha256"

    def hash_input(self, input: str) -> str:
        """
        Return a hash of inputted string

        @param input: string

        @return string - hashed string
        """

        return hashlib.new(self._hash_type, input.encode("utf-8")).hexdigest()
