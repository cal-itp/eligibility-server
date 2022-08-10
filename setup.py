import csv
import json

from flask_sqlalchemy import inspect
from eligibility_server import app
import logging


logger = logging.getLogger("setup")


def import_users():
    """
    Imports user data to be added to database and saves user to database

    Users can be imported from either a JSON file or CSV file, as configured
    with settings from environment variables. CSV files take extra setting
    configurations: CSV_DELIMITER, CSV_NEWLINE, CSV_QUOTING, CSV_QUOTECHAR
    """

    logger.info(f"Importing users from {app.app.config["IMPORT_FILE_PATH"]}")
    if app.app.config["IMPORT_FILE_FORMAT"] == "json":
        with open(app.app.config["IMPORT_FILE_PATH"]) as file:
            data = json.load(file)["users"]
            for user in data:
                save_users(user, data[user][0], str(data[user][1]))
    elif app.app.config["IMPORT_FILE_FORMAT"] == "csv":
        with open(app.app.config["IMPORT_FILE_PATH"], newline=app.app.config["CSV_NEWLINE"], encoding="utf-8") as file:
            data = csv.reader(
                file,
                delimiter=app.app.config["CSV_DELIMITER"],
                quoting=int(app.app.config["CSV_QUOTING"]),
                quotechar=app.app.config["CSV_QUOTECHAR"],
            )
            for user in data:
                save_users(user[0], user[1], user[2])
    else:
        file_format = app.app.config["IMPORT_FILE_FORMAT"]
        logger.warning(f"File format is not supported: {file_format}")

    logger.info(f"Users added: {app.User.query.count()}")


def save_users(user_id: str, key: str, types: str):
    """
    Add users to the database User table

    @param user_id - User's ID, not to be confused with Database row ID
    @param key - User's key
    @param types - Types of eligibilities, in a stringified list
    """

    item = app.User(user_id=user_id, key=key, types=types)
    app.db.session.add(item)
    app.db.session.commit()


if __name__ == "__main__":
    inspector = inspect(app.db.engine)

    if inspector.get_table_names():
        logger.info("Tables already exist.")
        if app.User.query.count() == 0:
            import_users()
        else:
            logger.info("User table already has data.")
    else:
        logger.info("Creating table...")
        app.db.create_all()
        logger.info("Table created.")
        import_users()
