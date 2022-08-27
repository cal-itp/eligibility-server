import click
from flask import current_app
from flask_sqlalchemy import inspect

from .models import db, User


@click.command("drop-db")
def drop_db_command():
    with current_app.app_context():
        inspector = inspect(db.engine)

        if inspector.get_table_names():
            try:
                click.echo(f"Users to be deleted: {User.query.count()}")
                User.query.delete()
                db.session.commit()
            except Exception as e:
                click.echo("Failed to query for Users", e)

            db.drop_all()
            click.echo("Database dropped.")
        else:
            click.echo("Database does not exist.")
