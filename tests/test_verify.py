import json
import pytest
import uuid

from eligibility_server.verify import Verify


def test_Verify_client_get_unauthorized_request(client):
    response = client.get("/verify")

    assert response.status_code == 403
    assert response.content_type == "application/json"
    assert response.json["message"] == "Forbidden"


def test_Verify_client_get_bad_request(mocker, client):
    token_payload = dict(sub="A1234567", name="Garcia", eligibility=["type1"])
    mocked_headers = {"TOKEN_HEADER": "blah"}
    mocker.patch("eligibility_server.verify.Verify._check_headers", return_value=mocked_headers)
    mocker.patch("eligibility_server.verify.Verify._get_token", return_value="token")
    mocker.patch("eligibility_server.verify.Verify._get_token_payload", return_value="bad token")
    response = client.get("/verify", json=token_payload)

    assert response.status_code == 400
    assert response.content_type == "application/json"
    assert response.json["message"].startswith("Bad request")


@pytest.mark.usefixtures("flask")
def test_Verify_get_response_sub_format_match(mocker):
    mocked_config = {"SUB_FORMAT_REGEX": r"^[A-Z]\d{7}$", "INPUT_HASH_ALGO": ""}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    token_payload = json.loads(json.dumps(dict(sub="A1234567", name="Garcia", eligibility=["type1"], jti=str(uuid.uuid4()))))

    _, response_code = Verify()._get_response(token_payload)

    assert response_code == 200


@pytest.mark.usefixtures("flask")
def test_Verify_get_response_sub_format_no_match(mocker):
    mocked_config = {"SUB_FORMAT_REGEX": r"^[A-Z]\d{7}$", "INPUT_HASH_ALGO": ""}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    # "sub" value does not match the format regex
    token_payload = json.loads(json.dumps(dict(sub="nomatch", name="Garcia", eligibility=["type1"], jti=str(uuid.uuid4()))))

    _, response_code = Verify()._get_response(token_payload)

    assert response_code == 400


def test_Verify_init_keypair():
    verify = Verify()

    assert verify.client_public_key
    assert verify.server_private_key


# todo: this should really be driven by a test database instead
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
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    verify = Verify()
    assert verify._check_user(sub, name, types) == expected
