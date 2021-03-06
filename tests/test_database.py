"""
Test database class and methods
"""
import pytest


from eligibility_server.database import Database
from eligibility_server.hash import Hash


test_data = [
    (Database(), "A1234567", "Garcia", ["type1"], ["type1"]),  # This key/user pair is in the database
    (Database(), "A1234567", "Garcia", ["type2"], []),  # This key/user pair does not have "type2" in its associated array
    (Database(), "A1234567", "Aaron", ["type1"], []),  # This key/user pair does not exist
    (Database(), "G7778889", "Thomas", ["type1"], []),  # User not in database
    (Database(Hash("sha256")), "A1234568", "Garcia", ["type1"], ["type1"]),  # Correct key/user pair and correct hash algo type
    (Database(Hash("sha256")), "A1234568", "Garcia", ["type2"], []),  # This key/user pair does not have "type2" in its array
    (Database(Hash("sha256")), "A1234568", "Aaron", ["type1"], []),  # This key/user pair does not exist
    (Database(Hash("sha256")), "G7778889", "Thomas", ["type1"], []),  # User does not exist
    (Database(Hash("sha512")), "D4567891", "James", ["type1"], ["type1"]),  # Specific hash algo type
    (Database(Hash("sha256")), "D4567891", "James", ["type1"], []),  # Wrong hash algo type
]


def test_database_init_default():
    database = Database()

    assert database._users
    assert database._hash is False


@pytest.mark.databasetest
@pytest.mark.parametrize("db, key, user, types, expected", test_data)
def test_database_check_user(db, key, user, types, expected):
    assert db.check_user(key, user, types) == expected
