import json
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


def test_Verify_get_response_sub_format_match(mocker, mock_config):
    mocked_config = mock_config({"SUB_FORMAT_REGEX": r"^[A-Z]\d{7}$", "INPUT_HASH_ALGO": ""})
    mocker.patch("eligibility_server.verify.app.app.config", new=mocked_config)
    mocker.patch("eligibility_server.verify.Verify._make_token", return_value="token")
    token_payload = json.loads(json.dumps(dict(sub="A1234567", name="Garcia", eligibility=["type1"], jti=str(uuid.uuid4()))))

    response = Verify()._get_response(token_payload)

    assert response[1] == 200


def test_Verify_get_response_sub_format_no_match(mocker, mock_config):
    mocked_config = mock_config({"SUB_FORMAT_REGEX": r"^[A-Z]\d{7}$", "INPUT_HASH_ALGO": ""})
    mocker.patch("eligibility_server.verify.app.app.config", new=mocked_config)
    mocker.patch("eligibility_server.verify.Verify._make_token", return_value="token")
    # "sub" value does not match the format regex
    token_payload = json.loads(json.dumps(dict(sub="nomatch", name="Garcia", eligibility=["type1"], jti=str(uuid.uuid4()))))

    response = Verify()._get_response(token_payload)

    assert response[1] == 400
