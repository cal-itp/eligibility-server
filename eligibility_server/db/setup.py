import ast  # needed while sample CSV contains Python-style list
import csv
import json

import click
from flask import current_app
from flask_sqlalchemy import inspect

from eligibility_server.db import db
from eligibility_server.db.models import User, Eligibility
from eligibility_server.settings import Configuration


config = Configuration()


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
    with settings. CSV files take extra setting configurations:
    CSV_DELIMITER, CSV_NEWLINE, CSV_QUOTING, CSV_QUOTECHAR
    """

    file_path = config.import_file_path
    click.echo(f"Importing users from {file_path}")

    file_format = file_path.split(".")[-1]

    if file_format == "json":
        with open(file_path) as file:
            data = json.load(file)["users"]
            for user in data:
                save_users(user, data[user][0], data[user][1])
    elif file_format == "csv":
        with open(file_path, newline=config.csv_newline, encoding="utf-8") as file:
            data = csv.reader(
                file,
                delimiter=config.csv_delimiter,
                quoting=config.csv_quoting,
                quotechar=config.csv_quotechar,
            )
            for user in data:
                # todo: update sample CSV to use expected list format and change this parsing
                types = ast.literal_eval(user[2])
                save_users(user[0], user[1], types)
    else:
        click.echo(f"Warning: File format is not supported: {file_format}")

    click.echo(f"Users added: {User.query.count()}")
    click.echo(f"Eligibility types added: {Eligibility.query.count()}")


def save_users(sub: str, name: str, types):
    """
    Add users to the database User table

    @param sub - User's sub
    @param name - User's name
    @param types - Types of eligibilities, in a stringified list
    """

    user = User(sub=sub, name=name)
    eligibility_types = [Eligibility.query.filter_by(name=type).first() or Eligibility(name=type) for type in types]
    user.types.extend(eligibility_types)

    db.session.add(user)
    db.session.add_all(eligibility_types)

    db.session.commit()


@click.command("drop-db")
def drop_db_command():
    with current_app.app_context():
        inspector = inspect(db.engine)

        if inspector.get_table_names():
            try:
                click.echo(f"Users to be deleted: {User.query.count()}")
                User.query.delete()

                click.echo(f"Eligibility types to be deleted: {Eligibility.query.count()}")
                Eligibility.query.delete()

                db.session.commit()
            except Exception as e:
                click.echo("Failed to query for Users", e)

            db.drop_all()
            click.echo("Database dropped.")
        else:
            click.echo("Database does not exist.")
