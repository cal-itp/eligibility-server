import csv
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import os
from tempfile import NamedTemporaryFile

import click
from flask import current_app
from sqlalchemy import column, inspect
import requests

from eligibility_server.db import db
from eligibility_server.db.models import User, Eligibility, Metadata
from eligibility_server.settings import Configuration


config = Configuration()


@click.command("init-db")
def init_db_command():
    file_mtime = None
    with current_app.app_context():
        inspector = inspect(db.engine)

        if inspector.get_table_names():
            click.echo("Tables already exist.")
            if User.query.count() == 0:
                file_mtime = import_users()
            else:
                click.echo("User table already has data.")
                # retrieve existing file_ts so we don't pass None to update_metadata
                existing_md = Metadata.query.first()
                if existing_md:
                    file_mtime = existing_md.file_ts
        else:
            click.echo("Creating table...")
            db.create_all()
            click.echo("Table created.")
            file_mtime = import_users()

    update_metadata(file_mtime=file_mtime)


def import_users() -> str:
    """
    Imports user data to database, from either a local or remote CSV file,
    given the `IMPORT_FILE_PATH` setting.
    CSV files take extra settings: `CSV_DELIMITER`, `CSV_QUOTING`, `CSV_QUOTECHAR`
    """

    path = config.import_file_path
    click.echo(f"Importing users from: {path}")

    format = path.split(".")[-1].lower()
    remote = path.lower().startswith("http")

    if format not in ["csv"]:
        click.warning(f"File format is not supported: {format}")
        return

    file_mtime = None
    if format == "csv":
        file_mtime = import_csv_users(path, remote)

    click.echo(f"Users added: {User.query.count()}")
    click.echo(f"Eligibility types added: {Eligibility.query.count()}")

    return file_mtime


def import_csv_users(csv_path, remote) -> str:
    # placeholder for a temp file that remote is downloaded to
    temp_csv = None
    file_mtime = None

    if remote:
        # download the content as text and write to a temp file
        # attempt to read a header indicating the last modified time of the file
        response = requests.get(csv_path, timeout=config.request_timeout)
        content = response.text

        # try the Last-Modified header first, falling back to the Date header
        header_date = response.headers.get("Last-Modified") or response.headers.get("Date")
        if header_date:
            try:
                # parsedate_to_datetime handles the RFC 2822 format common for response headers
                dt = parsedate_to_datetime(header_date)
                file_mtime = dt.astimezone(timezone.utc).isoformat(timespec="seconds")
            except Exception:
                pass

        # note we leave the temp file open so it exists later for reading
        temp_csv = NamedTemporaryFile(mode="w", encoding="utf-8")
        temp_csv.write(content)
        # reset the file pointer to the beginning for reading, and reset path
        temp_csv.seek(0)
        csv_path = temp_csv.name
    else:
        # for local files, read the last modified time
        if os.path.exists(csv_path):
            mtime = os.path.getmtime(csv_path)
            file_mtime = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat(timespec="seconds")

    # open the file and read it with a csv.reader
    # open in read mode explicitly since the file may still be open if we downloaded from remote
    # newline="" is important here, see https://docs.python.org/3/library/csv.html#id3
    with open(csv_path, mode="r", encoding="utf-8", newline="") as file:
        data = csv.DictReader(
            file,
            delimiter=config.csv_delimiter,
            quoting=config.csv_quoting,
            quotechar=config.csv_quotechar if config.csv_quotechar else None,
        )

        for row in data:
            # type lists are expected to be a comma-separated value and quoted if the CSV delimiter is a comma
            types = row["type"]
            types = [t.replace(config.csv_quotechar, "") for t in types.split(",") if t]
            save_user(row["sub"], row["name"], types)

    # close and remove the temp file if needed
    if temp_csv:
        temp_csv.close()

    return file_mtime


def save_user(sub: str, name: str, types: list):
    """
    Add a user to the database User table

    @param sub - User's sub
    @param name - User's name
    @param types - Types of eligibilities, in the form of a list of strings
    """

    user = User.query.filter_by(sub=sub, name=name).first() or User(sub=sub, name=name)
    eligibility_types = [Eligibility.query.filter_by(name=t).first() or Eligibility(name=t) for t in types]
    new_types = [t for t in eligibility_types if t not in user.types]

    if any(new_types):
        user.types.extend(new_types)
        db.session.add_all(new_types)

    db.session.add(user)
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

            except Exception as e:
                click.echo(f"Failed to query models. Exception: {e}", err=True)

            db.session.commit()

            db.drop_all()
            click.echo("Database dropped.")
        else:
            click.echo("Database does not exist.")


def update_metadata(file_mtime: str = None):
    Metadata.query.delete()

    ts = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
    users = User.query.count()
    eligibility = [e.name for e in Eligibility.query.add_columns(column("name"))]

    metadata = Metadata(load_ts=ts, file_ts=file_mtime, users=users, eligibility=eligibility)
    db.session.add(metadata)
    db.session.commit()

    click.echo("Database metadata updated.")
