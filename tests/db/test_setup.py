from datetime import datetime, timedelta, timezone
import os

import pytest
from sqlalchemy import inspect

from eligibility_server.db import db
from eligibility_server.db.models import Eligibility, Metadata, User


@pytest.fixture
def mock_csv_file(tmp_path):
    """Creates a temporary CSV file for testing local imports."""
    d = tmp_path / "data"
    d.mkdir()
    f = d / "test_users.csv"
    # Content matches expected CSV columns
    content = "sub,name,type\n12345,Tester,agency_card"
    f.write_text(content)
    return f


@pytest.fixture(autouse=True)
def patch_import_file_path(mocker, mock_csv_file):
    # Patch config to point to the temp file
    mocker.patch("eligibility_server.settings.Configuration.import_file_path", str(mock_csv_file))


@pytest.mark.usefixtures("flask")
class TestDatabaseCommands:

    def test_init_db_captures_local_mtime(self, runner, mock_csv_file, flask):
        """Verify file_ts reflects the local filesystem modification time."""
        # Set a specific mtime for the file (2 hours ago)
        past_time = datetime.now(tz=timezone.utc) - timedelta(hours=2)
        os.utime(mock_csv_file, (past_time.timestamp(), past_time.timestamp()))

        runner.invoke(args="drop-db")
        result = runner.invoke(args="init-db")

        assert result.exit_code == 0
        with flask.app_context():
            metadata = Metadata.query.first()
            # file_ts should match the file's modification time
            assert metadata.file_ts == past_time.isoformat(timespec="seconds")
            # load_ts should be 'now'
            load_dt = datetime.fromisoformat(metadata.load_ts)
            assert datetime.now(tz=timezone.utc) - load_dt < timedelta(seconds=2)

    def test_init_db_captures_remote_header(self, runner, mocker, flask):
        """Verify file_ts reflects the HTTP headers for remote files."""
        # re-patch to a "remote" file
        mocker.patch("eligibility_server.settings.Configuration.import_file_path", "http://fake.com/data.csv")

        # Mock requests.get to return custom headers
        mock_response = mocker.Mock()
        mock_response.text = "sub,name,type\n54321,RemoteUser,agency_card"
        # Simulating the header format found in the manual HEAD check
        mock_response.headers = {"Date": "Tue, 23 Dec 2025 18:18:06 GMT"}
        mocker.patch("requests.get", return_value=mock_response)

        runner.invoke(args="drop-db")
        runner.invoke(args="init-db")

        with flask.app_context():
            metadata = Metadata.query.first()
            # Verify timezone conversion from HTTP GMT to ISO format
            assert metadata.file_ts == "2025-12-23T18:18:06+00:00"

    def test_data_integrity_and_eligibility(self, runner, flask):
        """Ensure users and their eligibility types are correctly linked."""
        runner.invoke(args="drop-db")
        runner.invoke(args="init-db")

        with flask.app_context():
            user = User.query.filter_by(sub="12345").first()
            assert user is not None
            assert user.name == "Tester"
            # Verify that Eligibility model is correctly populated and linked
            assert len(user.types) == 1
            assert user.types[0].name == "agency_card"

    def test_idempotency_and_metadata_overwrite(self, runner, flask):
        """Ensure running init-db twice updates metadata but prevents duplicates."""
        runner.invoke(args="drop-db")
        runner.invoke(args="init-db")

        # Second Run
        result = runner.invoke(args="init-db")
        assert result.exit_code == 0

        with flask.app_context():
            # User check ensures save_user filter logic works
            assert User.query.count() == 1
            # Eligibility check ensures no duplicates are created
            assert Eligibility.query.count() == 1
            # Metadata check ensures update_metadata delete logic works
            assert Metadata.query.count() == 1

    def test_drop_db_command(self, runner, flask):
        """Verify drop-db clears all tables and data."""
        runner.invoke(args="init-db")

        # Execute drop
        result = runner.invoke(args="drop-db")
        assert result.exit_code == 0
        assert "Database dropped." in result.output

        with flask.app_context():
            inspector = inspect(db.engine)
            # SQLAlchemy inspect should show no tables exist
            assert inspector.get_table_names() == []

    def test_drop_db_empty_state(self, runner):
        """Verify drop-db handles a non-existent database gracefully."""
        runner.invoke(args="drop-db")

        # Run again
        result = runner.invoke(args="drop-db")
        assert result.exit_code == 0
        assert "Database does not exist." in result.output
