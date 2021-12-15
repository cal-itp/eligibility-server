"""
Test database class and methods
"""

import json

with open("data/server.json", encoding="utf8") as file:
    DATA = json.load(file)


def test_database_init(database):
    assert database._users


def test_database_check_user_in_database(database):
    key = "A1234567"
    user = "Garcia"
    types = ["type1"]

    response = database.check_user(key, user, types)

    assert response == types


def test_database_check_user_in_database_not_eligible(database):
    key = "A1234567"
    user = "Garcia"
    types = ["type2"]  # This key/user pair does not have "type2" in its associated array

    response = database.check_user(key, user, types, False)

    assert response == []


def test_database_check_user_in_database_not_found(database):
    key = "A1234567"
    user = "Aaron"  # This key/user pair does not exist
    types = ["type1"]

    response = database.check_user(key, user, types, False)

    assert response == []


def test_database_check_user_not_in_database(database):
    response = database.check_user("G7778889", "Thomas", ["type1"])

    assert response == []


def test_database_check_user_in_database_with_hashing(database):
    key = "A1234568"
    user = "Garcia"
    types = ["type1"]

    response = database.check_user(key, user, types, True)

    assert response == types


def test_database_check_ineligible_user_in_database_with_hashing(database):
    key = "A1234568"
    user = "Garcia"
    types = ["type2"]  # This key/user pair does not have "type2" in its associated array

    response = database.check_user(key, user, types, True)

    assert response == []


def test_database_check_ineligible_user_not_found_in_database_with_hashing(database):
    key = "A1234568"
    user = "Aaron"  # This key/user pair does not exist
    types = ["type1"]

    response = database.check_user(key, user, types, True)

    assert response == []


def test_database_check_user_not_in_database_with_hashing(database):
    response = database.check_user("G7778889", "Thomas", ["type1"], True)

    assert response == []


def test_database_check_user_in_database_with_hashing_specific_type(database):
    key = "D4567891"
    user = "James"
    types = ["type1", "type2"]

    response = database.check_user(key, user, types, True, "sha512")

    assert response == types
