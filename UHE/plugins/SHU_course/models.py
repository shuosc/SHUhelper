import datetime

from flask import abort
from flask_login import UserMixin
from mongoengine import (BooleanField, DateTimeField, EmailField, DecimalField, ReferenceField,
                         StringField, IntField)

from UHE.client import Services
from UHE.extensions import db


class Course(db.Document):
    no = StringField()
    name = StringField()
    teacher = StringField()
    credit = StringField()
    liked = IntField(default=0)
    comments = IntField(default=0)

    def __unicode__(self):
        return '{}-{}-{}'.format(self.name, self.no, self.teacher)


class CourseOfTerm(db.Document):
    course = ReferenceField(Course)
    teacher_no = StringField()
    time = StringField()
    place = StringField()
    capacity = IntField()
    enroll = IntField()
    campus = StringField()
    q_time = StringField()
    q_place = StringField()
    school = StringField()
    tag = StringField()
    term = StringField()
    updated = BooleanField(default=True)
