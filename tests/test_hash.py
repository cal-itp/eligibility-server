"""
Test hash class method
"""

from eligibility_server import settings


def test_hash_init(hash):
    assert settings.HASH_TYPE == "sha256"
    if settings.HASH_INPUTS:
        assert True


def test_hash_input_default(hash):
    """
    Tests hash_input with HASH_TYPE set to sha256 and HASH_INPUTS to true
    """
    hashed_string = hash.hash_input("Test")

    assert hashed_string == "532eaabd9574880dbf76b9b8cc00832c20a6ec113d682299550d7a6e0f345e25"  # noqa: E501


# def test_hash_false():
#     # hashed_string = Hash.hash_input("Test", False, "sha256")
#     hashed_string = Hash.hash_input("Test")

#     assert hashed_string == "Test"


# def test_hash_input_sha512():
#     # hashed_string = Hash.hash_input("Test", True, "sha512")
#     hashed_string = Hash.hash_input("Test")

#     assert (
#         hashed_string
#         == "c6ee9e33cf5c6715a1d148fd73f7318884b41adcb916021e2bc0e800a5c5dd97f5142178f6ae88c8fdd98e1afb0ce4c8d2c54b5f37b30b7da1997bb33b0b8a31"  # noqa: E501
#     )


# def test_hash_input_whirlpool():
#     # hashed_string = Hash.hash_input("Test", True, "whirlpool")
#     hashed_string = Hash.hash_input("Test")

#     assert (
#         hashed_string
#         == "ac1c196e84b05d59faea639d0cccb6c16f7568e0943f4c94c648bd8eefe5cf3978f8d4f99b1426e4ce3c6fa40e17cf68d6b86d42246333569b963ff4579c6355"  # noqa: E501
#     )
