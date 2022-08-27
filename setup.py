import csv
import json
import logging

from flask_sqlalchemy import inspect

from eligibility_server.app import app
from eligibility_server.database import db, User


logger = logging.getLogger("setup")


def import_users():
    """
    Imports user data to be added to database and saves user to database

    Users can be imported from either a JSON file or CSV file, as configured
    with settings from environment variables. CSV files take extra setting
    configurations: CSV_DELIMITER, CSV_NEWLINE, CSV_QUOTING, CSV_QUOTECHAR
    """

    file_path = app.config["IMPORT_FILE_PATH"]
    logger.info(f"Importing users from {file_path}")

    file_format = file_path.split(".")[-1]

    if file_format == "json":
        with open(file_path) as file:
            data = json.load(file)["users"]
            for user in data:
                save_users(user, data[user][0], str(data[user][1]))
    elif file_format == "csv":
        with open(file_path, newline=app.config["CSV_NEWLINE"], encoding="utf-8") as file:
            data = csv.reader(
                file,
                delimiter=app.config["CSV_DELIMITER"],
                quoting=int(app.config["CSV_QUOTING"]),
                quotechar=app.config["CSV_QUOTECHAR"],
            )
            for user in data:
                save_users(user[0], user[1], user[2])
    else:
        logger.warning(f"File format is not supported: {file_format}")

    logger.info(f"Users added: {User.query.count()}")


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


if __name__ == "__main__":
    with app.app_context():
        inspector = inspect(db.engine)

        if inspector.get_table_names():
            logger.info("Tables already exist.")
            if User.query.count() == 0:
                import_users()
            else:
                logger.info("User table already has data.")
        else:
            logger.info("Creating table...")
            db.create_all()
            logger.info("Table created.")
            import_users()
