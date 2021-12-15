"""
Test database class and methods
"""

import json

with open("data/server.json", encoding="utf8") as file:
    DATA = json.load(file)


def test_database_init(database):
    assert database._users


def test_database_check_user_in_database(database):
    key = min(DATA["users"])
    user = DATA["users"][key][0]
    types = DATA["users"][key][1]

    response = database.check_user(key, user, types)

    assert response == types


def test_database_check_user_in_database_not_eligible(database):
    key = min(DATA["users"])
    user = DATA["users"][key][0]
    types = ["type2"]

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
