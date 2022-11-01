import pytest

from flask_sqlalchemy import inspect
from eligibility_server.db import db
from eligibility_server.db.models import Eligibility, User


@pytest.mark.usefixtures("flask")
def test_init_db_command(runner):
    """Assumes that IMPORT_FILE_PATH is data/server.csv."""
    runner.invoke(args="drop-db")

    result = runner.invoke(args="init-db")

    assert result.exit_code == 0

    assert User.query.count() == 24
    assert Eligibility.query.count() == 1

    user_with_one_eligibility = User.query.filter_by(sub="32587", name="Gonzales").first()
    courtesy_card_type = Eligibility.query.filter_by(name="courtesy_card").first()
    assert user_with_one_eligibility.types == [courtesy_card_type]


@pytest.mark.usefixtures("flask")
def test_drop_db_command(runner):
    result = runner.invoke(args="drop-db")

    assert result.exit_code == 0

    inspector = inspect(db.engine)
    assert inspector.get_table_names() == []

    # temp fix to ensure database tests are idempotent - later tests need the database to exist
    runner.invoke(args="init-db")
