"""
Simple Test Eligibility Verification API Server.
"""

import json

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from . import settings
from .verify import Verify


app = Flask(__name__)
app.name = settings.APP_NAME
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), unique=True, nullable=False)
    key = db.Column(db.String(120), unique=True, nullable=False)
    types = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.user_id


@app.route("/healthcheck")
def healthcheck():
    return "Healthy"


def create_users():
    print("create_users()")
    with open("data/server.json") as f:
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


api = Api(app)
api.add_resource(Verify, "/verify")


if __name__ == "__main__":
    app.run(host=settings.HOST, debug=settings.DEBUG_MODE)  # nosec
    # Run this file directly to create the database tables.
