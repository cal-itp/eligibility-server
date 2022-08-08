"""
Simple Test Eligibility Verification API Server.
"""

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from logging.config import dictConfig

from . import settings
from .verify import Verify

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s %(name)s:%(lineno)s %(message)s",
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
app.name = settings.APP_NAME
app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS


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
    app.run(host=settings.HOST, debug=settings.DEBUG_MODE)  # nosec
