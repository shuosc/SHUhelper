import datetime
from flask_login import current_user
from application.extensions import db
from application.models.user import User


class Course(db.Model):
    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    course_id = db.Column(db.String)
    name = db.Column(db.String)
    credit = db.Column(db.String)
    detail = db.Column(db.String)
    dept = db.Column(db.String)
    created = db.Column(db.DateTime, nullable=False,
                           default=datetime.now)
    updated = db.Column(db.DateTime, nullable=False,
                           default=datetime.now)

class CourseClass(db.Model):
    id = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    teacher_id = db.Column(db.String)
    teacher_name_raw = db.Column(db.String, db.ForeignKey('teacher.id'))
    course_id =  db.Column(db.String, db.ForeignKey('course.id'))
    capacity = db.Column(db.Integer)
    enroll = db.Column(db.Integer)
    time = db.Column(db.String)
    campus = db.Column(db.String)
    q_time = db.Column(db.String)
    q_place = db.Column(db.String)
    class_id = db.Column(db.String)
    year = db.Column(db.Integer)
    term = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable=False,
                           default=datetime.now)
    updated = db.Column(db.DateTime, nullable=False,
                           default=datetime.now)


