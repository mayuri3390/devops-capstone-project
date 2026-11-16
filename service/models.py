import logging
from datetime import date
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")
db = SQLAlchemy()


class DataValidationError(Exception):
    pass


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(32), nullable=True)
    date_joined = db.Column(db.Date(), nullable=False, default=date.today())

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def create(self):
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat(),
        }

    def deserialize(self, data):
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data["address"]
            self.phone_number = data.get("phone_number")
            dj = data.get("date_joined")
            self.date_joined = date.fromisoformat(dj) if dj else date.today()
        except KeyError as err:
            raise DataValidationError("Invalid Account: missing " + err.args[0]) from err
        except TypeError as err:
            raise DataValidationError("Invalid Account: bad data - " + err.args[0]) from err
        return self

    @classmethod
    def init_db(cls, app):
        db.init_app(app)
        app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name == name)
