import json
import tempfile

import setup


def test_import_users(mocker, mock_config, flask, database):
    # set up an import file for the test
    with tempfile.NamedTemporaryFile("w", suffix=".json") as import_file:
        users = json.dumps({"users": {"A1234567": ["Garcia", ["type1"]]}})
        import_file.write(users)
        import_file.flush()

        # make sure the setup module uses the test import file
        mocked_config = mock_config({"IMPORT_FILE_PATH": import_file.name})
        mocker.patch("setup.app.app.config", new=mocked_config)

        # make sure the setup module uses fixture app instead of the real one
        mocker.patch("setup.app.app", flask)

        setup.import_users()

        # the problem here is that User and Eligibility are models defined on the real app's db
        assert flask.User.query.count() == 1
        assert flask.Eligibility.query.count() == 1
