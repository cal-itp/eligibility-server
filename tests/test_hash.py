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
    (
        "whirlpool",
        "ac1c196e84b05d59faea639d0cccb6c16f7568e0943f4c94c648bd8eefe5cf3978f8d4f99b1426e4ce3c6fa40e17cf68d6b86d42246333569b963ff4579c6355",  # noqa: E501
    ),
]


def test_hash_init():
    assert Hash("whirlpool")._input_hash_algo == "whirlpool"


def test_hash_init_invalid_type():
    with pytest.raises(ValueError):
        Hash("thing")


def test_hash_init_invalid_blank():
    with pytest.raises(TypeError):
        Hash()


@pytest.mark.parametrize("hash_input_algo, expected", test_data)
def test_hash_input(hash_input_algo, expected):
    assert Hash(hash_input_algo).hash_input("Test") == expected
