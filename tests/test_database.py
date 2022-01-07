"""
Test database class and methods
"""

import json


with open("data/server.json", encoding="utf8") as file:
    DATA = json.load(file)


def test_database_init(database):
    assert database._users


def test_database_check_user_in_database(database):
    # This test is currently failing, because HASH_INPUTS is set to True
    # This test should pass when HASH_INPUTS is set to False
    key = "A1234567"
    user = "Garcia"
    types = ["type1"]

    response = database.check_user(key, user, types)

    assert response == types


def test_database_check_user_in_database_not_eligible(database):
    key = "A1234567"
    user = "Garcia"
    types = ["type2"]  # This key/user pair does not have "type2" in its associated array

    response = database.check_user(key, user, types)

    assert response == []


def test_database_check_user_in_database_not_found(database):
    key = "A1234567"
    user = "Aaron"  # This key/user pair does not exist
    types = ["type1"]

    response = database.check_user(key, user, types)

    assert response == []


def test_database_check_user_not_in_database(database):
    response = database.check_user("G7778889", "Thomas", ["type1"])

    assert response == []


def test_database_check_user_in_database_with_hashing(database):
    key = "A1234568"
    user = "Garcia"
    types = ["type1"]

    response = database.check_user(key, user, types)

    assert response == types


def test_database_check_ineligible_user_in_database_with_hashing(database):
    key = "A1234568"
    user = "Garcia"
    types = ["type2"]  # This key/user pair does not have "type2" in its associated array

    response = database.check_user(key, user, types)

    assert response == []


def test_database_check_ineligible_user_not_found_in_database_with_hashing(database):
    key = "A1234568"
    user = "Aaron"  # This key/user pair does not exist
    types = ["type1"]

    response = database.check_user(key, user, types)

    assert response == []


def test_database_check_user_not_in_database_with_hashing(database):
    response = database.check_user("G7778889", "Thomas", ["type1"])

    assert response == []


def test_database_check_user_in_database_with_hashing_specific_type(database):
    # settings.HASH_TYPE == "sha512"
    # This test is currently failing because HASH_TYPE needs to be
    # set to "sha512"
    key = "D4567891"
    user = "James"
    types = ["type1"]

    response = database.check_user(key, user, types)

    assert response == types
