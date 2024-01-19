from core import db
from core.libs import helpers
from core.libs.models import FyleBaseModel


class User(FyleBaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, db.Sequence('users_id_seq'), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)



    @classmethod
    def get_by_email(cls, email):
        return cls.filter(cls.email == email).first()
