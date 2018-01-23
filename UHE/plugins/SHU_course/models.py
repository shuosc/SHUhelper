import datetime

from flask import abort
from flask_login import UserMixin
from mongoengine import (BooleanField, DateTimeField, EmailField, DecimalField, ReferenceField, ListField, PULL, CASCADE,
                         StringField, IntField,URLField,EmbeddedDocument,SortedListField,EmbeddedDocumentField,FloatField,EmbeddedDocumentListField)

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
    comments = EmbeddedDocumentListField(Comment,default=lambda: [])
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

# unique_with='teacher',
class Course(db.Document):
    no = StringField(required=True)
    name = StringField(required=True)
    teacher = ReferenceField(Teacher,required=True)
    teacher_name = StringField(required=True)
    credit = StringField()
    detail = StringField(default="")
    target = StringField(default="")
    like = ListField(ReferenceField(User, deref=True), default=lambda: [])
    like_count = IntField(default=0)
    refrences = StringField(default="")
    evaluations = EmbeddedDocumentListField(Evaluation, default=lambda: [])
    rating = FloatField(default=lambda: 0,required=True)
    school = StringField(required=True)
    category = StringField(default="")
    tags = ListField(StringField(), default=lambda: [])
    terms = SortedListField(StringField(), reverse=True,default=lambda: [],required=True)
    meta = {
        'strict': False
    }

    def __unicode__(self):
        return '{}-{}-{}'.format(self.name, self.no, self.teacher)

class CourseOfTerm(db.Document):
    course = ReferenceField(Course,reverse_delete_rule=CASCADE)
    course_no = StringField(required=True)
    course_name = StringField(required=True)
    credit = StringField(required=True)
    teacher = ReferenceField(Teacher,required=True)
    teacher_no = StringField(required=True)
    teacher_name = StringField(required=True)
    time = StringField()
    place = StringField()
    capacity = IntField(default=0)
    enroll = IntField(default=0)
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
