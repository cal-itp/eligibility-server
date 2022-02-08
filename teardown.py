from eligibility_server import app

if __name__ == "__main__":
    print(app.User.query.count(), "users to be deleted.")
    app.User.query.delete()
    app.db.session.commit()
    app.db.drop_all()
    print("Database dropped.")
