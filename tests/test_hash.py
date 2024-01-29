"""
Test hash class method
"""

import pytest

from eligibility_server.hash import Hash


test_data = [
    ("sha256", "532eaabd9574880dbf76b9b8cc00832c20a6ec113d682299550d7a6e0f345e25"),
    (
        "sha512",
        "c6ee9e33cf5c6715a1d148fd73f7318884b41adcb916021e2bc0e800a5c5dd97f5142178f6ae88c8fdd98e1afb0ce4c8d2c54b5f37b30b7da1997bb33b0b8a31",  # noqa: E501
    ),
]


def test_hash_init():
    assert Hash("sha512")._input_hash_algo == "sha512"


def test_hash_init_invalid_type():
    with pytest.raises(ValueError):
        Hash("thing")


def test_hash_init_invalid_blank():
    with pytest.raises(TypeError):
        Hash()


@pytest.mark.parametrize("hash_input_algo, expected", test_data)
def test_hash_input(hash_input_algo, expected):
    assert Hash(hash_input_algo).hash_input("Test") == expected
