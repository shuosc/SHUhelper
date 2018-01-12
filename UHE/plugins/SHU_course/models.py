import datetime

from flask import abort
from flask_login import UserMixin
from mongoengine import (BooleanField, DateTimeField, EmailField, DecimalField, ReferenceField, ListField, PULL, CASCADE,
                         StringField, IntField)

from UHE.client import Services
from UHE.extensions import db
# from UHE.comment.models import Comment


class Course(db.Document):
    no = StringField()
    name = StringField()
    teacher = StringField()
    credit = StringField()
    liked = IntField(default=0)
    # comments = ListField(ReferenceField(
    #     Comment, reverse_delete_rule=PULL), default=lambda: [])
    school = StringField()
    tag = ListField(StringField())
    this_term = BooleanField(default=False)
    remark = StringField(default='')
    meta = {
        'strict': False
    }

    def __unicode__(self):
        return '{}-{}-{}'.format(self.name, self.no, self.teacher)


class CourseOfTerm(db.Document):
    course = ReferenceField(Course, reverse_delete_rule=CASCADE)
    teacher_no = StringField()
    time = StringField()
    place = StringField()
    capacity = IntField()
    enroll = IntField()
    campus = StringField()
    q_time = StringField()
    q_place = StringField()
    term = StringField()
    updated = BooleanField(default=True)
    meta = {
        'strict': False
    }
