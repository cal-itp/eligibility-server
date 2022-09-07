"""
Test database class and methods
"""
import pytest


from eligibility_server.verify import Verify


test_data = [
    ("", "A1234567", "Garcia", ["type1"], ["type1"]),  # This sub/name pair is in the database
    ("", "A1234567", "Garcia", ["type2"], []),  # This sub/name pair does not have "type2" in its associated array
    ("", "A1234567", "Aaron", ["type1"], []),  # This sub/name pair does not exist
    ("", "G7778889", "Thomas", ["type1"], []),  # User not in Hash
    ("sha256", "A1234568", "Garcia", ["type1"], ["type1"]),  # Correct sub/name pair and correct hash algo type
    ("sha256", "A1234568", "Garcia", ["type2"], []),  # This sub/name pair does not have "type2" in its array
    ("sha256", "A1234568", "Aaron", ["type1"], []),  # This sub/name pair does not exist
    ("sha256", "G7778889", "Thomas", ["type1"], []),  # name does not exist
    ("sha512", "D4567891", "James", ["type1"], ["type1"]),  # Specific hash algo type
    ("sha256", "D4567891", "James", ["type1"], []),  # Wrong hash algo type
]


@pytest.mark.usefixtures("flask")
@pytest.mark.parametrize("hash, sub, name, types, expected", test_data)
def test_check_user(mocker, hash, sub, name, types, expected):
    mocked_config = {"INPUT_HASH_ALGO": hash}
    mocker.patch.dict("eligibility_server.verify.current_app.config", mocked_config)

    verify = Verify()
    assert verify._check_user(sub, name, types) == expected
