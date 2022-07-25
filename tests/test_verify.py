import json
import uuid

from eligibility_server.verify import Verify


def test_Verify_get_response():
    token_payload = json.loads(json.dumps(dict(sub="A1234567", name="Garcia", eligibility=["type1"], jti=str(uuid.uuid4()))))

    response = Verify()._get_response(token_payload)

    assert response[1] == 200
