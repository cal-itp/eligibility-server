import logging

from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    types = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.sub
