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
