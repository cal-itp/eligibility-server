import csv
import json

from eligibility_server import app, settings


def import_users():
    print("Importing users from", settings.IMPORT_FILE_PATH)
    if settings.IMPORT_FILE_FORMAT == "json":
        with open(settings.IMPORT_FILE_PATH) as file:
            data = json.load(file)["users"]
            for user in data:
                save_users(user, data[user][0], str(data[user][1]))
    if settings.IMPORT_FILE_FORMAT == "csv":
        with open(settings.IMPORT_FILE_PATH, newline="", encoding="utf-8") as file:
            data = csv.reader(file, delimiter=";", quotechar="", quoting=csv.QUOTE_NONE)
            for user in data:
                save_users(user[0], user[1], user[2])


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
    print("Creating table...")
    app.db.create_all()
    print("Table created.")
    import_users(app.db, app.User)
    print(app.User.query.count(), "users added.")
