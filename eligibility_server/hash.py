"""
Hashing tool.
"""

import hashlib


class Hash:
    def hash_input(input, hash_inputs, hash_type):
        """
        Return a hash of inputted string

        @param input: string
        @param hash_inputs: boolean - default False, set in settings
        @param hash_type: optional, string of hashlib available algorithms defaults to 'sha256', set in settings
        options: 'sha256', 'sha384', 'sha512' and others

        @return string - hashed string
        """

        if hash_inputs:
            return hashlib.new(hash_type, input.encode("utf-8")).hexdigest()

        return input
