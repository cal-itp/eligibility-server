from eligibility_server import app

db = app.db
User = app.User

if __name__ == "__main__":
    print(User.query.count(), "users to be deleted.")
    User.query.delete()
    db.session.commit()
    db.drop_all()
    print("Database dropped.")
