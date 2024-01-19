from core import db
from core.libs import helpers
from core.libs.exceptions import FyleError
from core.libs.models import FyleBaseModel

class Teacher(FyleBaseModel):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, db.Sequence('teachers_id_seq'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    @classmethod
    def get_by_id(cls, id):
        # Added to for test coverage.
        teacher = cls.query.filter_by(id=id).first()
        if teacher is None:
            fyleError =  FyleError("No teacher with this id was found", 404)
            result = fyleError.to_dict()
            raise FyleError(result['message'], result['status_code'])
        return teacher


    @classmethod
    def get_teachers_by_principal(cls):
        """
        Get all teachers associated with a principal.
        """
        return cls.filter().all()