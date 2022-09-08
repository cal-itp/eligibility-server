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

    assert User.query.count() == 6
    assert Eligibility.query.count() == 2

    user_with_one_eligibility = User.query.filter_by(sub="A1234567", name="Garcia").first()
    type1_eligibility = Eligibility.query.filter_by(name="type1").first()
    assert user_with_one_eligibility.types == [type1_eligibility]

    user_with_no_eligibility = User.query.filter_by(sub="C3456789", name="Smith").first()
    assert user_with_no_eligibility.types == []

    user_with_multiple_eligibilities = User.query.filter_by(sub="D4567890", name="Jones").first()
    type2_eligibility = Eligibility.query.filter_by(name="type2").first()
    assert user_with_multiple_eligibilities.types == [type1_eligibility, type2_eligibility]


@pytest.mark.usefixtures("flask")
def test_drop_db_command(runner):
    result = runner.invoke(args="drop-db")

    assert result.exit_code == 0

    inspector = inspect(db.engine)
    assert inspector.get_table_names() == []
