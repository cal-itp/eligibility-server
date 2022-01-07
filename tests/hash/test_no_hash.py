"""
Test hash class method
"""

import os


def test_hash_init(hash):
    assert os.environ.get("HASH_INPUTS") == "false"
    assert os.environ.get("HASH_TYPE") == ""
    assert hash._hash_type == ""
    assert hash._hash_inputs == False  # noqa e712


def test_hash_false(hash):
    hashed_string = hash.hash_input("Test")

    assert hashed_string == "Test"


def test_database_check_user_in_database(database):
    # This test is currently failing, because HASH_INPUTS is set to True
    # This test should pass when HASH_INPUTS is set to False
    key = "A1234567"
    user = "Garcia"
    types = ["type1"]

    response = database.check_user(key, user, types)

    assert response == types
