"""
Hashing tool.
"""

import hashlib
import logging


logger = logging.getLogger(__name__)


class Hash:
    def __init__(self, input_hash_algo: str):
        """
        Initialize Hash object and validate hash type
        """

        algorithms_available = hashlib.algorithms_available

        if input_hash_algo in algorithms_available:
            self._input_hash_algo = input_hash_algo
            logger.info(f"Input hash algorithm set to: {input_hash_algo}")
        else:
            raise ValueError("Invalid input_hash_algo, must be one of: " + (" ").join(algorithms_available))

    def hash_input(self, input: str) -> str:
        """
        Return a hash of inputted string, encoded in UTF-8, and in hexdigest format
        """

        return hashlib.new(self._input_hash_algo, input.encode("utf-8")).hexdigest()
