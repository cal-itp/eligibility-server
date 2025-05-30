from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import inspect

from eligibility_server.db import db
from eligibility_server.db.models import Eligibility, Metadata, User


@pytest.mark.usefixtures("flask")
def test_init_db_command(runner):
    """Assumes that IMPORT_FILE_PATH is data/server.csv."""
    runner.invoke(args="drop-db")

    start_time = datetime.now(tz=timezone.utc)
    result = runner.invoke(args="init-db")

    assert result.exit_code == 0

    assert User.query.count() == 26
    assert Eligibility.query.count() == 1
    assert Metadata.query.count() == 1

    metadata = Metadata.query.first()
    assert metadata.users == User.query.count()
    assert datetime.fromisoformat(metadata.timestamp) - start_time < timedelta(seconds=1)
    assert metadata.eligibility == ["agency_card"]

    user_with_one_eligibility = User.query.filter_by(sub="32587", name="Gonzales").first()
    agency_card_type = Eligibility.query.filter_by(name="agency_card").first()
    assert user_with_one_eligibility.types == [agency_card_type]


@pytest.mark.usefixtures("flask")
def test_drop_db_command(runner):
    result = runner.invoke(args="drop-db")

    assert result.exit_code == 0

    inspector = inspect(db.engine)
    assert inspector.get_table_names() == []

    # temp fix to ensure database tests are idempotent - later tests need the database to exist
    runner.invoke(args="init-db")
