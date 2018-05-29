from datetime import datetime
from flask_login import current_user
from application.extensions import db, ma
import uuid
from marshmallow import post_load

# from application.models.user import UndergraduateStudentSchema as StudentSchema
from application.utils import CRUDMixin, TimeMixin
from marshmallow import fields
from application.models.user import User

class StudentClass(db.Model, CRUDMixin, TimeMixin):
    student_id = db.Column(db.String, db.ForeignKey(
        'undergraduate_student.id'), primary_key=True)
    class_id = db.Column(db.UUID(as_uuid=True),
                         db.ForeignKey('class.id'), primary_key=True)
    grade_1 = db.Column(db.Integer)
    grade_2 = db.Column(db.Integer)
    _class = db.relationship("Class", back_populates="students")
    student = db.relationship("UndergraduateStudent",back_populates="classes")


class Class(db.Model, CRUDMixin, TimeMixin):
    id = db.Column(db.UUID(as_uuid=True),
                   default=uuid.uuid4, primary_key=True)
    course_id = db.Column(db.String, db.ForeignKey(
        'course.id'))
    term = db.Column(db.String)
    class_id = db.Column(db.String)
    teacher_id = db.Column(db.String, db.ForeignKey('teacher.id'))
    teacher_raw = db.Column(db.String)
    time = db.Column(db.String)
    classroom = db.Column(db.String)
    capacity = db.Column(db.Integer, default=0)
    enroll = db.Column(db.Integer, default=0)
    campus = db.Column(db.String)
    q_time = db.Column(db.String)
    q_place = db.Column(db.String)
    credit = db.Column(db.String)
    status = db.Column(db.String)
    students = db.relationship('StudentClass', back_populates="_class")
    __table_args__ = (db.UniqueConstraint('class_id', 'course_id', 'term'),)


class UndergraduateStudent(User):
    __tablename__ = 'undergraduate_student'
    id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    # classes = db.relationship('Class', secondary=student_classes, lazy='subquery',
    #    backref=db.backref('dtudents', lazy=True))
    classes = db.relationship('StudentClass', back_populates="student")
    __mapper_args__ = {
        'polymorphic_identity': 'undergraduate_student',
    }

    def __unicode__(self):
        return self.name


class UndergraduateStudentSchema(ma.ModelSchema):
    # oauth = ma.List()
    class Meta:
        model = UndergraduateStudent
        exclude = ('oauth', 'pw_hash')

    @post_load
    def load(self, data):
        return UndergraduateStudent(**data)


undergraduate_student_schema = UndergraduateStudentSchema()
undergraduate_students_schema = UndergraduateStudentSchema(many=True)


class Teacher(User):
    __tablename__ = 'teacher'
    id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    degree = db.Column(db.String())
    sex = db.Column(db.String())
    title = db.Column(db.String())
    education = db.Column(db.String())
    dept = db.Column(db.String())
    cs = db.Column(db.String())
    intro = db.Column(db.String())
    classes = db.relationship(Class, backref='teacher', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }

    def __unicode__(self):
        return self.name


class TeacherSchema(ma.ModelSchema):
    # oauth = ma.List()
    class Meta:
        model = Teacher
        exclude = ('oauth', 'pw_hash')

    @post_load
    def load(self, data):
        return Teacher(**data)


teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)

class ClassSchema(ma.ModelSchema):
    students = ma.Nested('StudentSchema', many=True)
    course = ma.Nested('CourseSchema')
    class_id = ma.String(data_key="classID")
    q_time = ma.String(data_key="qTime")
    q_place = fields.String(data_key="qPlace")
    teacher = ma.Nested('TeacherSchema')
    course_id = ma.String(data_key="courseID")
    teacher_id = ma.String(data_key="teacherID")

    class Meta:
        model = Class
        include_fk = True
        # exclude = ('students',)

    # @post_load
    # def load(self, data):
    #     print(self)
    #     return Class(**data)


class_schema = ClassSchema()
classes_schema = ClassSchema(many=True)


class Course(db.Model, CRUDMixin, TimeMixin):
    # id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    credit = db.Column(db.String)
    detail = db.Column(db.String)
    dept = db.Column(db.String)
    classes = db.relationship('Class', backref='course', lazy=True)

    @classmethod
    def from_json(cls, json_post):
        return cls(
            id=json_post.get('id'),
            name=json_post.get('name'),
            credit=json_post.get('credit'),
            detail=json_post.get('detail')
        )

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'credit': self.credit
        }


class CourseSchema(ma.ModelSchema):
    class Meta:
        model = Course

    @post_load
    def load(self, data):
        return Course(**data)


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
