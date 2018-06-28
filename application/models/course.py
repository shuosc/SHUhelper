from datetime import datetime
from flask_login import current_user
from application.extensions import db, ma
import uuid
from marshmallow import post_load

# from application.models.user import UndergraduateStudentSchema as StudentSchema
from application.utils import CRUDMixin, TimeMixin
from marshmallow import fields
from application.models.user import User



class Class(db.Model, CRUDMixin, TimeMixin):
    id = db.Column(db.UUID(as_uuid=True),
                   default=uuid.uuid4, primary_key=True)
    course_id = db.Column(db.String, db.ForeignKey(
        'course.id'), index=True)
    term = db.Column(db.String, index=True)
    class_id = db.Column(db.String, index=True)
    teacher_id = db.Column(db.String, db.ForeignKey('teacher.id'), index=True)
    teacher_raw = db.Column(db.String)
    time = db.Column(db.String, index=True)
    classroom = db.Column(db.String)
    capacity = db.Column(db.Integer, default=0, index=True)
    enroll = db.Column(db.Integer, default=0)
    campus = db.Column(db.String, index=True)
    q_time = db.Column(db.String)
    q_place = db.Column(db.String)
    credit = db.Column(db.String, index=True)
    status = db.Column(db.String)
    techer = db.relationship(Teacher, backref='classes')
    __table_args__ = (db.UniqueConstraint('class_id', 'course_id', 'term'),)


class ClassSchema(ma.ModelSchema):
    students = ma.Nested('StudentClassSchema', many=True,
                         only=('grade_1', 'grade_2', 'grade', 'point','student','class_id'))
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
    name = db.Column(db.String, index=True)
    credit = db.Column(db.String, index=True)
    detail = db.Column(db.String)
    dept = db.Column(db.String)
    classes = db.relationship('Class', backref='course', lazy=True)
    extra = db.Column(db.JSON)
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
