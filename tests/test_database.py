"""
Test database class and methods
"""

from eligibility_server.database import Database as Database
from eligibility_server.hash import Hash as Hash


def test_database_init_default():
    database = Database()

    assert database._users
    assert database._hash is False


def test_database_check_user_in_database():
    key = "A1234567"
    user = "Garcia"
    types = ["type1"]
    database = Database()

    response = database.check_user(key, user, types)

    assert response == types


def test_database_check_user_in_database_not_eligible():
    key = "A1234567"
    user = "Garcia"
    types = ["type2"]  # This key/user pair does not have "type2" in its associated array
    database = Database()

    response = database.check_user(key, user, types)

    assert response == []


def test_database_check_user_in_database_not_found():
    key = "A1234567"
    user = "Aaron"  # This key/user pair does not exist
    types = ["type1"]
    database = Database()

    response = database.check_user(key, user, types)

    assert response == []


def test_database_check_user_not_in_database():
    database = Database()

    response = database.check_user("G7778889", "Thomas", ["type1"])

    assert response == []


def test_database_check_user_in_database_with_hashing():
    key = "A1234568"
    user = "Garcia"
    types = ["type1"]
    database = Database(Hash("sha256"))

    response = database.check_user(key, user, types)

    assert response == types


def test_database_check_ineligible_user_in_database_with_hashing():
    key = "A1234568"
    user = "Garcia"
    types = ["type2"]  # This key/user pair does not have "type2" in its associated array
    database = Database(Hash("sha256"))

    response = database.check_user(key, user, types)

    assert response == []


def test_database_check_ineligible_user_not_found_in_database_with_hashing():
    key = "A1234568"
    user = "Aaron"  # This key/user pair does not exist
    types = ["type1"]
    database = Database(Hash("sha256"))

    response = database.check_user(key, user, types)

    assert response == []


def test_database_check_user_not_in_database_with_hashing():
    database = Database(Hash("sha256"))

    response = database.check_user("G7778889", "Thomas", ["type1"])

    assert response == []


def test_database_check_user_in_database_with_hashing_specific_type():
    key = "D4567891"
    user = "James"
    types = ["type1"]
    database = Database(Hash("sha512"))

    response = database.check_user(key, user, types)

    assert response == types
