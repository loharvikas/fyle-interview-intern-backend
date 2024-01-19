from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from flask_migrate import Migrate

from sqlalchemy.engine import Engine
from flask import jsonify
from core.libs import helpers
from marshmallow.exceptions import ValidationError
from sqlite3 import Connection as SQLite3Connection
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from .config import DevConfig




db = SQLAlchemy()
# this is to enforce fk (not done by default in sqlite3)
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()






def create_app(config_class=DevConfig) -> Flask:
    """
    Creates a Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    db.init_app(app)
    migrate = Migrate(app, db)
    from core.apis.assignments import student_assignments_resources, teacher_assignments_resources, principal_assignments_resources
    from core.apis.teachers import principal_teachers_resources, teachers_resources
    
    app.register_blueprint(student_assignments_resources, url_prefix='/student')
    app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
    app.register_blueprint(principal_assignments_resources, url_prefix='/principal')
    app.register_blueprint(principal_teachers_resources, url_prefix='/principal')
    app.register_blueprint(teachers_resources, url_prefix='/teacher')


    @app.route('/')
    def ready():
        """
        Check if the server is ready(Used for health check).
        """
        response = jsonify({
            'status': 'ready',
            'time': helpers.get_utc_now()
        })

        return response
    
    @app.errorhandler(Exception)
    def handle_error(err):
        if isinstance(err, FyleError):
            return jsonify(
                error=err.__class__.__name__, message=err.message
            ), err.status_code
        elif isinstance(err, ValidationError):
            return jsonify(
                error=err.__class__.__name__, message=err.messages
            ), 400
        elif isinstance(err, IntegrityError):
            return jsonify(
                error=err.__class__.__name__, message=str(err.orig)
            ), 400
        elif isinstance(err, HTTPException):
            return jsonify(
                error=err.__class__.__name__, message=str(err)
            ), err.code

        raise err


    return app