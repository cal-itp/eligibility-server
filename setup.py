import json

from eligibility_server import app, settings

db = app.db
User = app.User


def import_users(db, User):
    print("importing users from", settings.IMPORT_FILEPATH)
    with open(settings.IMPORT_FILEPATH) as f:
        data = json.load(f)
        print(data)
        for user in data["users"]:
            user_id = user
            key = data["users"][user][0]
            types = str(data["users"][user][1])
            row = User(user_id=user_id, key=key, types=str(types))
            print(row)
            db.session.add(row)
            db.session.commit()
    print(User.query.all())


if __name__ == "__main__":
    print("Creating tables...")
    db.create_all()
    print("Tables created!")
    import_users(db, User)
    print("Users added")
