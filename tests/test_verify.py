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
    mocker.patch("eligibility_server.verify.get_token_payload", return_value="bad token")
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
    # This sub/name pair is in the database
    ("", "32587", "Gonzales", ["courtesy_card"], ["courtesy_card"]),
    # This sub/name pair does not have the type
    ("", "32587", "Gonzales", ["something"], []),
    # This sub/name pair does not exist
    ("", "12345", "Aaron", ["courtesy_card"], []),
    # Correct sub/name pair and correct hash algo type
    ("sha512", "89768", "Muñoz", ["courtesy_card"], ["courtesy_card"]),
    # This sub/name pair does not have the type
    ("sha512", "89768", "Muñoz", ["something"], []),
    # This sub/name pair does not exist
    ("sha512", "12345", "Smith", ["courtesy_card"], []),
    # Wrong hash algo type
    ("sha256", "89768", "Muñoz", ["courtesy_card"], []),
]


@pytest.mark.usefixtures("flask")
@pytest.mark.parametrize("hash, sub, name, types, expected", test_data)
def test_check_user(mocker, hash, sub, name, types, expected):
    mocked_config = {"INPUT_HASH_ALGO": hash}
    mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

    verify = Verify()
    assert verify._check_user(sub, name, types) == expected
