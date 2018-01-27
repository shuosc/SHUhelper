import datetime

from mongoengine import (BooleanField, DateTimeField, ReferenceField, ListField, CASCADE,
                         StringField, IntField, URLField, SortedListField, FloatField, EmbeddedDocumentListField)

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
    teacher = ReferenceField(Teacher, required=True)
    teacher_name = StringField(required=True)
    credit = StringField()
    detail = StringField(default="")
    target = StringField(default="")
    like = ListField(ReferenceField(User, deref=True), default=lambda: [])
    like_count = IntField(default=0)
    refrences = StringField(default="")
    heat = IntField(default=0)
    evaluations_count = IntField(default=0)
    # evaluations = ListField(ReferenceField(Evaluation), default=lambda: [])
    rating = FloatField(default=lambda: 0, required=True)
    school = StringField(required=True)
    category = StringField(default="")
    tags = ListField(StringField(), default=lambda: [])
    terms = SortedListField(StringField(), reverse=True,
                            default=lambda: [])
    meta = {
        'strict': False,
        'ordering': ['-heat'],
        'indexes': [
            'heat',
            'credit',
            'no',
            'name',
            'teacher_name'
        ]
    }

    def __unicode__(self):
        return '{}-{}-{}'.format(self.name, self.no, self.teacher)



class Evaluation(db.Document):
    user = ReferenceField(User)
    display_name = StringField()
    text = StringField(default='')
    course = ReferenceField(Course)
    term = StringField()
    like = ListField(ReferenceField(User, deref=True), default=lambda: [])
    liked_count = IntField()
    rating = IntField()
    comments = EmbeddedDocumentListField(Comment, default=lambda: [])
    deleted = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.now)
    meta = {
        'ordering': ['-created'],
        'strict': False,
        'indexes': [
            'course',
            'created'
        ]
    }

    def to_dict(self):
        return {
            'display_name': self.display_name,
            'text': self.text,
            'course': {
                'id': str(self.course.id),
                'no': self.course.no,
                'name': self.course.name,
                'teacherName': self.course.teacher_name},
            'term': self.term,
            'like': self.like,
            'rating': self.rating,
            'created': str(self.created)
        }


class CourseOfTerm(db.Document):
    course = ReferenceField(Course, reverse_delete_rule=CASCADE)
    course_no = StringField(required=True)
    course_name = StringField(required=True)
    credit = StringField(required=True)
    teacher = ReferenceField(Teacher, required=True)
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
            'course_no',
            'course_name',
            'teacher_name',
            'time',
            '#term',
            '#credit',
            '#campus'
        ]
    }

class CourseSelectedRecord(db.Document):
    course = ReferenceField(CourseOfTerm)
    enroll = ListField(IntField(),default=lambda: [])
    capacity = ListField(IntField(),default=lambda: [])
    updated = ListField(DateTimeField(),default=lambda: [])
