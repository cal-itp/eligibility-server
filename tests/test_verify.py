import json
import uuid

import pytest

from eligibility_server.verify import Verify


@pytest.mark.skip(reason="Need to fix mocking")
def test_Verify_get_response_sub_format_match(mocker):
    # mocker.patch("eligibility_server.app.config["SUB_FORMAT_REGEX"]", r"^[A-Z]\d{7}$")
    token_payload = json.loads(json.dumps(dict(sub="A1234567", name="Garcia", eligibility=["type1"], jti=str(uuid.uuid4()))))

    response = Verify()._get_response(token_payload)

    assert response[1] == 200


@pytest.mark.skip(reason="Need to fix mocking")
def test_Verify_get_response_sub_format_no_match(mocker):
    # mocker.patch("eligibility_server.app.config["SUB_FORMAT_REGEX"]", r"^[A-Z]\d{7}$")
    # "sub" value does not match the format regex
    token_payload = json.loads(json.dumps(dict(sub="nomatch", name="Garcia", eligibility=["type1"], jti=str(uuid.uuid4()))))

    response = Verify()._get_response(token_payload)

    assert response[1] == 400
