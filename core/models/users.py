from sqlite3 import IntegrityError
from core import db
from core.libs import helpers
from core.libs.models import FyleBaseModel


class User(FyleBaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, db.Sequence('users_id_seq'), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)



    @classmethod
    def get_by_email(cls, email:str) -> 'User':
        return cls.filter(cls.email == email).first()
    
    @classmethod
    def get_by_username(cls, username:str) -> 'User':
        return cls.filter(cls.username == username).first()

    
    @classmethod
    def create(cls, email:str,username:str) -> 'User':
        """
        Create a new user.
        """
        if cls.get_by_email(email):
            raise IntegrityError('User with this email already exists')
        if cls.get_by_username(username):
            raise IntegrityError('User with this username already exists')
        user = User(email=email, username=username)
        db.session.add(user)
        db.session.flush()
        return user