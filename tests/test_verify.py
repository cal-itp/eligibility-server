import json
import uuid

import pytest

from eligibility_server.db import db
from eligibility_server.db.models import User, Eligibility
from eligibility_server.hash import Hash
from eligibility_server.verify import Verify


@pytest.fixture(autouse=True)
def setup_db(flask):
    """Initialize the database schema before each test."""
    with flask.app_context():
        db.create_all()
    yield
    with flask.app_context():
        db.drop_all()


@pytest.fixture
def seed_db(flask):
    """
    Seeds the database with specific users, applying hashing if configured
    for the current test case.
    """

    def _seed(hash_algo=""):
        with flask.app_context():
            # Clear existing data to ensure isolation
            User.query.delete()
            Eligibility.query.delete()

            sub1, name1 = "32587", "Gonzales"
            sub2, name2 = "89768", "Muñoz"

            # Apply hashing if an algorithm is provided
            if hash_algo:
                h = Hash(hash_algo)
                sub1, name1 = h.hash_input(sub1), h.hash_input(name1)
                sub2, name2 = h.hash_input(sub2), h.hash_input(name2)

            user1 = User(sub=sub1, name=name1)
            user2 = User(sub=sub2, name=name2)

            # The relationship between User and Eligibility models
            type_agency = Eligibility(name="agency_card")
            user1.types.append(type_agency)
            user2.types.append(type_agency)

            db.session.add_all([user1, user2, type_agency])
            db.session.commit()

    return _seed


@pytest.mark.usefixtures("flask")
class TestVerify:

    def test_client_get_unauthorized_request(self, client):
        response = client.get("/verify")

        assert response.status_code == 403
        assert response.content_type == "application/json"
        assert response.json["message"] == "Forbidden"

    def test_client_get_bad_request(self, mocker, client):
        token_payload = dict(sub="A1234567", name="Garcia", eligibility=["type1"])
        mocked_headers = {"TOKEN_HEADER": "blah"}
        mocker.patch("eligibility_server.verify.Verify._check_headers", return_value=mocked_headers)
        mocker.patch("eligibility_server.verify.Verify._get_token", return_value="token")
        mocker.patch("eligibility_server.verify.get_token_payload", return_value="bad token")
        response = client.get("/verify", json=token_payload)

        assert response.status_code == 400
        assert response.content_type == "application/json"
        assert response.json["message"].startswith("Bad request")

    def test_get_response_sub_format_match(self, mocker, seed_db):
        # Seed plain text for this test
        seed_db(hash_algo="")

        mocked_config = {"SUB_FORMAT_REGEX": r"^[A-Z]\d{7}$", "INPUT_HASH_ALGO": ""}
        mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

        token_payload = json.loads(
            json.dumps(dict(sub="A1234567", name="Garcia", eligibility=["type1"], jti=str(uuid.uuid4())))
        )

        # Verify response code is 200 even if user doesn't exist (format matches)
        _, response_code = Verify()._get_response(token_payload)
        assert response_code == 200

    def test_get_response_sub_format_no_match(self, mocker):
        mocked_config = {"SUB_FORMAT_REGEX": r"^[A-Z]\d{7}$", "INPUT_HASH_ALGO": ""}
        mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

        # "sub" value does not match the format regex
        token_payload = json.loads(
            json.dumps(dict(sub="nomatch", name="Garcia", eligibility=["type1"], jti=str(uuid.uuid4())))
        )

        _, response_code = Verify()._get_response(token_payload)

        assert response_code == 400

    def test_init_keypair(self):
        verify = Verify()

        assert verify.client_public_key
        assert verify.server_private_key

    @pytest.mark.parametrize(
        "hash_algo, sub, name, types, expected",
        [
            ("", "32587", "Gonzales", ["agency_card"], ["agency_card"]),
            ("", "32587", "Gonzales", ["something"], []),
            ("", "12345", "Aaron", ["agency_card"], []),
            ("sha256", "89768", "Muñoz", ["agency_card"], ["agency_card"]),
            ("sha512", "89768", "Muñoz", ["agency_card"], ["agency_card"]),
            ("sha512", "89768", "Muñoz", ["something"], []),
        ],
    )
    def test_check_user(self, mocker, seed_db, hash_algo, sub, name, types, expected):
        """Verifies user eligibility against seeded database records."""
        # seed the database specifically for this parameter set
        seed_db(hash_algo=hash_algo)

        # mock the app config to use the target hash algorithm
        mocked_config = {"INPUT_HASH_ALGO": hash_algo}
        mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

        verify = Verify()
        assert verify._check_user(sub, name, types) == expected

    def test_check_user_hash_mismatch(self, mocker, seed_db):
        """
        Verify that if the DB is seeded with one hash but the app uses another,
        no user is found.
        """
        # Seed DB with sha256 hashes
        seed_db(hash_algo="sha256")

        # Configure app to hash inputs with sha512
        mocked_config = {"INPUT_HASH_ALGO": "sha512"}
        mocker.patch.dict("eligibility_server.settings.current_app.config", mocked_config)

        verify = Verify()

        # This should return an empty list because the sha512 hash of '32587'
        # won't match the sha256 hash stored in the DB.
        result = verify._check_user("32587", "Gonzales", ["agency_card"])
        assert result == []
