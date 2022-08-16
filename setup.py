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

    file_path = app.app.config["IMPORT_FILE_PATH"]
    logger.info(f"Importing users from {file_path}")

    file_format = file_path.split(".")[-1]

    if file_format == "json":
        with open(file_path) as file:
            data = json.load(file)["users"]
            for user in data:
                save_users(user, data[user][0], data[user][1])
    elif file_format == "csv":
        with open(file_path, newline=app.app.config["CSV_NEWLINE"], encoding="utf-8") as file:
            CSV_QUOTECHAR = app.app.config["CSV_QUOTECHAR"]
            data = csv.reader(
                file,
                delimiter=app.app.config["CSV_DELIMITER"],
                quoting=int(app.app.config["CSV_QUOTING"]),
                quotechar=CSV_QUOTECHAR,
            )
            for user in data:
                # lists are expected to be a comma-separated value and quoted if the CSV delimiter is a comma
                types = [type.replace(CSV_QUOTECHAR, "") for type in user[2].split(",") if type]
                save_users(user[0], user[1], types)
    else:
        logger.warning(f"File format is not supported: {file_format}")

    logger.info(f"Users added: {app.User.query.count()}")
    logger.info(f"Eligibility types added: {app.Eligibility.query.count()}")


def save_users(user_id: str, user_name: str, types):
    """
    Add users to the database User table

    @param user_id - User's ID, not to be confused with Database row ID
    @param key - User's key
    @param types - Types of eligibilities, in a stringified list
    """

    user = app.User(user_id=user_id, user_name=user_name)
    eligibility_types = [app.Eligibility.query.filter_by(name=type).first() or app.Eligibility(name=type) for type in types]
    user.types.extend(eligibility_types)

    app.db.session.add(user)
    app.db.session.add_all(eligibility_types)

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
