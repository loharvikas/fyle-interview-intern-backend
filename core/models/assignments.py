from core import db
from core.apis.decorators import AuthPrincipal
from core.libs import helpers, assertions
from core.models.teachers import Teacher
from core.models.students import Student
from sqlalchemy.types import Enum as BaseEnum
from core.enums.assignment import GradeEnum, AssignmentStateEnum
from core.libs.models import FyleBaseModel

class Assignment(FyleBaseModel):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, db.Sequence('assignments_id_seq'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable=True)
    content = db.Column(db.Text)
    grade = db.Column(BaseEnum(GradeEnum))
    state = db.Column(BaseEnum(AssignmentStateEnum), default=AssignmentStateEnum.DRAFT, nullable=False)

    '''
    Refactor: The business logic of this class should be moved to a service(specific for business logic) class.
              This class should only contain the database related logic. This will help in better testability and
              maintainability. Because, as the model and business logic grows, it will be difficult to maintain.
    '''

    @classmethod
    def upsert(cls, assignment_new: 'Assignment'):
        """
        If it is a new assignment, then insert it, otherwise update it.
        """
        assertions.assert_valid(assignment_new.content is not None and assignment_new.content != ''  , 'assignment with empty content cannot be saved')
        if assignment_new.id is not None:
            assignment = Assignment.get_by_id(assignment_new.id)
            assertions.assert_found(assignment, 'No assignment with this id was found')
            assertions.assert_valid(assignment.state == AssignmentStateEnum.DRAFT,
                                    'only assignment in draft state can be edited')
            assignment.content = assignment_new.content
        else:
            assignment = assignment_new
            db.session.add(assignment_new)

        db.session.flush()
        return assignment
    


    @classmethod
    def submit(cls, _id, teacher_id, auth_principal: AuthPrincipal):
        """
        Submit an assignment.
        """
        assignment = Assignment.get_by_id(_id)
        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(assignment.state == AssignmentStateEnum.DRAFT.value, 'only a draft assignment can be submitted')
        assertions.assert_valid(assignment.student_id == auth_principal.student_id, 'This assignment belongs to some other student')
        assertions.assert_valid(assignment.content is not None and assignment.content != ''  , 'assignment with empty content cannot be saved')

        assignment.teacher_id = teacher_id

        assignment.state = AssignmentStateEnum.SUBMITTED.value
        db.session.flush()

        return assignment


    @classmethod
    def mark_grade(cls, _id, grade, auth_principal: AuthPrincipal):
        """
        Mark grade for an assignment.
        """
        assignment = Assignment.get_by_id(_id)
        assertions.assert_found(assignment, 'No assignment with this id was found')
        # if user is a teacher, then he can grade only his own assignments.
        if auth_principal.teacher_id:
            assertions.assert_valid(auth_principal.principal_id is None and auth_principal.teacher_id == assignment.teacher_id, 'This assignment belongs to some other teacher')
        assertions.assert_valid(grade is not None or grade != '', 'assignment with empty grade cannot be graded')
        assertions.assert_valid(assignment.state in (AssignmentStateEnum.SUBMITTED.value, AssignmentStateEnum.GRADED.value), 'only submitted or graded assignment can be graded')
        assignment.grade = grade
        assignment.state = AssignmentStateEnum.GRADED
        db.session.flush()

        return assignment

    @classmethod
    def get_assignments_by_student(cls, student_id):
        """
        Get all assignments of a student.
        """
        return cls.filter(cls.student_id == student_id).all()
    

    @classmethod
    def get_assignments_by_teacher(cls, teacher_id):
        """
        Get all assignments of a teacher.
        """
        return cls.filter(cls.teacher_id == teacher_id).all()
    
    
    @classmethod
    def get_submited_or_graded_assignments_by_principal(cls):
        """
        Get all submitted or graded assignments of a teacher.
        """
        return cls.filter(cls.state.in_([AssignmentStateEnum.SUBMITTED.value,AssignmentStateEnum.GRADED.value])).all()


