import datetime
from flask_login import current_user
from application.extensions import db
from application.models.user import User
from application.extensions import ma
from application.utils import CRUDMixin, TimeMixin


class Course(db.Model, CRUDMixin, TimeMixin):
    # id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    credit = db.Column(db.String)
    detail = db.Column(db.String)
    dept = db.Column(db.String)

    @classmethod
    def from_json(cls, json_post):
        return cls(
            name=json_post.get('name'),
            credit=json_post.get('credit')
        )

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'credit': self.credit
        }


class CourseScheme(ma.Schema):
    class Meta:
        model = Course

    @post_load
    def load(self, data):
        return Course(**data)


course_schema = CourseScheme()
courses_schema = CourseScheme(many=True)


class CourseClass(db.Model, CRUDMixin, TimeMixin):
    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    teacher_id = db.Column(db.String, db.ForeignKey('teacher.id'))
    teacher_name_raw = db.Column(db.String)
    course_id = db.Column(db.String, db.ForeignKey('course.id'))
    capacity = db.Column(db.Integer)
    enroll = db.Column(db.Integer)
    time = db.Column(db.String)
    campus = db.Column(db.String)
    q_time = db.Column(db.String)
    q_place = db.Column(db.String)
    class_id = db.Column(db.String)
    year = db.Column(db.Integer)
    term = db.Column(db.Integer)

    @classmethod
    def from_json(cls, json_post):
        return cls(
            teacher_id=json_post.get('teacherID'),
            teacher_name_raw=json_post.get('teacherNameRaw'),
            course_id=json_post.get('courseID'),
            time=json_post.get('time'),
            campus=json_post.get('campus'),
            class_id=json_post.get('classID'),
            year=json_post.get('year'),
            term=json_post.get('term'))

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'credit': self.credit
        }


class CourseClassScheme(ma.Schema):
    class Meta:
        model = CourseClass

    @post_load
    def load(self, data):
        return CourseClass(**data)


course_class_schema = CourseClass()
course_classes_schema = CourseClass(many=True)


class StudentCourse(db.Model, CRUDMixin, TimeMixin):
    id = db.Column(db.UUID(as_uuid=True),
                   default=uuid.uuid4, primary_key=True)
    class_id = db.Column(db.UUID, db.ForeignKey('course_class.id'))
    student_id = db.Column(
        db.String, db.ForeignKey('undergraduate_student.id'))
    year = db.Column(db.Integer)
    term = db.Column(db.Integer)
    grade_1 = db.Column(db.Integer)
    grade_2 = db.Column(db.Integer)

    @classmethod
    def from_json(cls, json_post):
        return cls(
            name=json_post.get('name'),
            credit=json_post.get('credit')
        )

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'credit': self.credit
        }

    @property
    def grade(self):
        return grade_1 * 0.4 + grade * 0.6


class StudentCourseScheme(ma.Schema):
    class Meta:
        model = StudentCourse

    @post_load
    def load(self, data):
        return StudentCourse(**data)


student_course_schema = StudentCourse()
student_courses_schema = StudentCourse(many=True)
