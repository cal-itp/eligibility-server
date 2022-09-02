from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    types = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.sub
