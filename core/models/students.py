from core import db
from core.libs import helpers
from core.libs.models import FyleBaseModel


class Student(FyleBaseModel):
    __tablename__ = 'students'
    id = db.Column(db.Integer, db.Sequence('students_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

        