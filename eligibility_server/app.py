"""
Simple Test Eligibility Verification API Server.
"""

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from logging.config import dictConfig

from .verify import Verify

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s %(name)s:%(lineno)s %(message)s",
                "datefmt": "%d/%b/%Y %H:%M:%S",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
app.config.from_object("eligibility_server.settings")
app.config.from_envvar("ELIGIBILITY_SERVER_SETTINGS", silent=True)


@app.route("/healthcheck")
def healthcheck():
    app.logger.info("Healthcheck")
    return "Healthy"


api = Api(app)
api.add_resource(Verify, "/verify")

db = SQLAlchemy(app)


user_eligibility = db.Table(
    "user_eligibility",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("eligibility_id", db.Integer, db.ForeignKey("eligibility.id"), primary_key=True),
)


class Eligibility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Eligibility {self.name}>"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique=True, nullable=False)
    user_name = db.Column(db.String, unique=True, nullable=False)
    types = db.relationship("Eligibility", secondary=user_eligibility, lazy="subquery", backref=db.backref("users", lazy=True))

    def __repr__(self):
        return f"<User {self.user_id}>"


if __name__ == "__main__":
    app.run(host=app.config["HOST"], debug=app.config["DEBUG_MODE"])  # nosec
