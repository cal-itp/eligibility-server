import csv
import json

import click
from flask import current_app
from flask_sqlalchemy import inspect

from .models import db, User


@click.command("init-db")
def init_db_command():
    with current_app.app_context():
        inspector = inspect(db.engine)

        if inspector.get_table_names():
            click.echo("Tables already exist.")
            if User.query.count() == 0:
                import_users()
            else:
                click.echo("User table already has data.")
        else:
            click.echo("Creating table...")
            db.create_all()
            click.echo("Table created.")

            import_users()


def import_users():
    """
    Imports user data to be added to database and saves user to database

    Users can be imported from either a JSON file or CSV file, as configured
    with settings from environment variables. CSV files take extra setting
    configurations: CSV_DELIMITER, CSV_NEWLINE, CSV_QUOTING, CSV_QUOTECHAR
    """

    file_path = current_app.config["IMPORT_FILE_PATH"]
    click.echo(f"Importing users from {file_path}")

    file_format = file_path.split(".")[-1]

    if file_format == "json":
        with open(file_path) as file:
            data = json.load(file)["users"]
            for user in data:
                save_users(user, data[user][0], str(data[user][1]))
    elif file_format == "csv":
        with open(file_path, newline=current_app.config["CSV_NEWLINE"], encoding="utf-8") as file:
            data = csv.reader(
                file,
                delimiter=current_app.config["CSV_DELIMITER"],
                quoting=int(current_app.config["CSV_QUOTING"]),
                quotechar=current_app.config["CSV_QUOTECHAR"],
            )
            for user in data:
                save_users(user[0], user[1], user[2])
    else:
        click.echo(f"Warning: File format is not supported: {file_format}")

    click.echo(f"Users added: {User.query.count()}")


def save_users(sub: str, name: str, types: str):
    """
    Add users to the database User table

    @param sub - User's ID, not to be confused with Database row ID
    @param name - User's name
    @param types - Types of eligibilities, in a stringified list
    """

    item = User(sub=sub, name=name, types=types)
    db.session.add(item)
    db.session.commit()


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
