"""
Hashing tool.
"""

import hashlib

from . import settings


class Hash:
    def __init__(self):
        """
        Initialize variables (hash_inputs, hash_type) from settings.py variables
        """

        self._hash_inputs = settings.HASH_INPUTS or False
        self._hash_type = settings.HASH_TYPE or "sha256"

    def hash_input(self, input: str) -> str:
        """
        Return a hash of inputted string

        @param input: string

        @return string - hashed string
        """

        if self._hash_inputs:
            return hashlib.new(self._hash_type, input.encode("utf-8")).hexdigest()

        return input
