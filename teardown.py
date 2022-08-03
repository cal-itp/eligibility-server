from flask_sqlalchemy import inspect
from eligibility_server import app

if __name__ == "__main__":
    inspector = inspect(app.db.engine)

    if inspector.get_table_names():
        print(app.User.query.count(), "users to be deleted.")
        app.User.query.delete()
        app.db.session.commit()
        app.db.drop_all()
        print("Database dropped.")
    else:
        print("Database does not exist.")
