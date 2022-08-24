import builtins
import json
import uuid

from os.path import exists

import pytest

from eligibility_server.verify import Verify


@pytest.fixture
def open_spy(mocker):
    return mocker.spy(builtins, "open")


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


def test_Verify_get_response_sub_format_match(mocker):
    mocked_config = {"SUB_FORMAT_REGEX": r"^[A-Z]\d{7}$", "INPUT_HASH_ALGO": ""}
    mocker.patch.dict("eligibility_server.verify.app.app.config", mocked_config)

    token_payload = json.loads(json.dumps(dict(sub="A1234567", name="Garcia", eligibility=["type1"], jti=str(uuid.uuid4()))))

    _, response_code = Verify()._get_response(token_payload)

    assert response_code == 200


def test_Verify_get_response_sub_format_no_match(mocker):
    mocked_config = {"SUB_FORMAT_REGEX": r"^[A-Z]\d{7}$", "INPUT_HASH_ALGO": ""}
    mocker.patch.dict("eligibility_server.verify.app.app.config", mocked_config)

    # "sub" value does not match the format regex
    token_payload = json.loads(json.dumps(dict(sub="nomatch", name="Garcia", eligibility=["type1"], jti=str(uuid.uuid4()))))

    _, response_code = Verify()._get_response(token_payload)

    assert response_code == 400


@pytest.mark.parametrize("key_path_setting", ["CLIENT_KEY_PATH", "SERVER_KEY_PATH"])
def test_Verify_init_keypair_default(flask, mocker, open_spy, key_path_setting):
    assert key_path_setting in flask.config
    default_path = flask.config[key_path_setting]
    assert exists(default_path)

    verify = Verify()

    # check that there was a call to open the default path
    assert mocker.call(default_path, "rb") in open_spy.call_args_list

    if "CLIENT" in key_path_setting:
        assert verify.client_public_key
    elif "SERVER" in key_path_setting:
        assert verify.server_private_key
