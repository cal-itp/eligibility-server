"""
Simple Test Eligibility Verification API Server.
"""

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask.logging import default_handler

from . import logging
from .verify import Verify

app = Flask(__name__)
app.config.from_object("eligibility_server.settings")
app.config.from_envvar("ELIGIBILITY_SERVER_SETTINGS", silent=True)

logging.configure(app.config["LOG_LEVEL"])
# remove the default handler since we configured logging after creating the app
# https://flask.palletsprojects.com/en/2.2.x/logging/#removing-the-default-handler
app.logger.removeHandler(default_handler)


@app.route("/healthcheck")
def healthcheck():
    app.logger.info("Healthcheck")
    return "Healthy"


api = Api(app)
api.add_resource(Verify, "/verify")

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique=True, nullable=False)
    key = db.Column(db.String, unique=True, nullable=False)
    types = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.user_id


if __name__ == "__main__":
    app.run(host=app.config["HOST"], debug=app.config["DEBUG_MODE"])  # nosec
