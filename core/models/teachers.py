from sqlite3 import IntegrityError
from core import db
from core.libs import helpers
from core.libs.exceptions import FyleError
from core.libs.models import FyleBaseModel
from core.models.users import User
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
    

    @classmethod
    def create(cls, email:str,username:str) -> 'Teacher':
        """
        Create a new teacher.
        """
        # create a new user
        user = User.create(email=email, username=username)
        # create a new teacher
        teacher = Teacher(user_id=user.id)
        db.session.add(teacher)
        db.session.commit()
        return teacher