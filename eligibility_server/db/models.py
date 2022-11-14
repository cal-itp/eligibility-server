from eligibility_server.db import db


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
    sub = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    types = db.relationship("Eligibility", secondary=user_eligibility, lazy="subquery", backref=db.backref("users", lazy=True))

    def __repr__(self):
        return f"<User {self.sub}>"
