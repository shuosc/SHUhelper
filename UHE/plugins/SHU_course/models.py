import datetime

from flask import abort
from flask_login import UserMixin
from mongoengine import (BooleanField, DateTimeField, EmailField, DecimalField, ReferenceField, ListField, PULL, CASCADE,
                         StringField, IntField,URLField,EmbeddedDocument,EmbeddedDocumentField,FloatField)

from UHE.client import Services
from UHE.extensions import db
from UHE.user.models import User
# from UHE.comment.models import Comment



class Comment(db.EmbeddedDocument):
    user = ReferenceField(User)
    text = StringField(default='')
    term = StringField()
    liked = ListField(ReferenceField(User, deref=True), default=lambda: [])
    liked_count = IntField()
    reply = IntField(default=-1)
    deleted = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)
    meta = {
        'ordering': ['created'],
        'strict': False
    }

    def __unicode__(self):
        return self.content

    def to_dict(self):
        return {
            'user': self.user.to_dict_public(),
            'created': str(self.created),
            'text': self.text
        }

class Evaluation(db.EmbeddedDocument):
    user = ReferenceField(User)
    text = StringField(default='')
    term = StringField()
    liked = ListField(ReferenceField(User, deref=True), default=lambda: [])
    liked_count = IntField()
    rating = IntField()
    comments = ListField(EmbeddedDocumentField(Comment),default=lambda: [])
    deleted = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)
    meta = {
        'ordering': ['created'],
        'strict': False
    } 


class Teacher(db.Document):
    no = StringField(primary_key=True)
    degree = StringField()
    sex = StringField()
    title = StringField()
    education = StringField()
    name = StringField()
    dept = StringField()
    cs = URLField()
    intro = StringField()
    def __unicode__(self):
        return self.name


class Course(db.Document):
    no = StringField()
    name = StringField()
    teacher = ReferenceField(Teacher)
    # teacher = StringField()
    credit = StringField()
    detail = StringField()
    liked = ListField(ReferenceField(User, deref=True), default=lambda: [])
    liked_count = IntField()
    evaluations = ListField(EmbeddedDocumentField(Evaluation), default=lambda: [])
    rating = FloatField()
    school = StringField()
    tag = ListField(StringField())
    this_term = BooleanField(default=False)
    meta = {
        'strict': False
    }

    def __unicode__(self):
        return '{}-{}-{}'.format(self.name, self.no, self.teacher)


class CourseOfTerm(db.Document):
    course = ReferenceField(Course, reverse_delete_rule=CASCADE)
    course_no = StringField()
    course_name = StringField()
    credit = StringField()
    teacher = ReferenceField(Teacher)
    teacher_no = StringField()
    teacher_name = StringField()
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
        'strict': False,
        'indexes': [
            '#credit',
            '#campus'
        ]
    }
