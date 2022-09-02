import logging

from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)


db = SQLAlchemy()


def init_app(app):
    db.init_app(app)

    from .setup import init_db_command, drop_db_command

    app.cli.add_command(init_db_command)
    app.cli.add_command(drop_db_command)
