import csv
import json

from eligibility_server import app, settings

db = app.db
User = app.User


def import_users(db, User):
    print("Importing users from", settings.IMPORT_FILE_PATH)
    if settings.IMPORT_FILE_FORMAT == "json":
        with open(settings.IMPORT_FILE_PATH) as file:
            data = json.load(file)["users"]
            for user in data:
                save_users(db, User, user, data[user][0], str(data[user][1]))
    if settings.IMPORT_FILE_FORMAT == "csv":
        with open(settings.IMPORT_FILE_PATH, newline="", encoding="utf-8") as file:
            data = csv.reader(file, delimiter=";", quotechar="", quoting=csv.QUOTE_NONE)
            for user in data:
                save_users(db, User, user[0], user[1], user[2])


def save_users(db, User, user_id, key, types):
    item = User(user_id=user_id, key=key, types=types)
    db.session.add(item)
    db.session.commit()


if __name__ == "__main__":
    print("Creating table...")
    db.create_all()
    print("Table created.")
    import_users(db, User)
    print(User.query.count(), "users added.")
