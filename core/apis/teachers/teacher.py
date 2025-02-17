from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.apis.teachers.schema import TeacherSchema, TeacherCreatePayloadSchema
from core.models.teachers import Teacher

teachers_resources = Blueprint('teachers_resources', __name__)
@teachers_resources.route('/detail', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_teacher_detail(p:decorators.AuthPrincipal):
    # added for test coverage.
    teacher = Teacher.get_by_id(p.teacher_id)
    teachers_dump = TeacherSchema().dump(teacher)
    return APIResponse.respond(data=teachers_dump)

@teachers_resources.route('/create', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
def create_teacher(payload):
    """
    Create a new teacher.
    """
    payload = TeacherCreatePayloadSchema().load(payload)
    teacher = Teacher.create(email=payload.get('email'), username=payload.get('username'))
    teachers_dump = TeacherSchema().dump(teacher)
    return APIResponse.respond(data=teachers_dump)