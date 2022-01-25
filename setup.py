import json

from eligibility_server import app, settings

db = app.db
User = app.User


def import_users(db, User):
    print("Importing users from", settings.IMPORT_FILEPATH)
    with open(settings.IMPORT_FILEPATH) as f:
        data = json.load(f)
        for user in data["users"]:
            key = data["users"][user][0]
            types = str(data["users"][user][1])
            row = User(user_id=user, key=key, types=str(types))
            db.session.add(row)
            db.session.commit()


if __name__ == "__main__":
    print("Creating table...")
    db.create_all()
    print("Table created!")
    import_users(db, User)
    print("Users added!")
