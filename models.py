"""
define models
"""
import datetime

from flask_login import UserMixin
from mongoengine import (BooleanField, DateTimeField, Document, EmailField,
                         EmbeddedDocument, EmbeddedDocumentField, ImageField,
                         IntField, ListField, ReferenceField, StringField)
from config import db

class User(UserMixin, Document):
    """
    collection of users
    """
    email = EmailField()
    name = StringField()
    nickname = StringField()
    card_id = StringField()
    open_id = StringField()
    phone = StringField()
    role = StringField()
    create_time = DateTimeField(default=datetime.datetime.now)
    def __unicode__(self):
        return self.card_id + self.name
    def get_id(self):
        return self.card_id

class UserData(db.Document):
    """
    collection of user data, from query used as cache, data encrpted with aes
    """
    data = StringField()
    site = StringField()
    user = ReferenceField(User)
    last_modified = DateTimeField(default=datetime.datetime.now)

class Comment(db.EmbeddedDocument):
    name = StringField(max_length=20)
    content = StringField(max_length=450)
    create_time = DateTimeField(default=datetime.datetime.now)

class Messages(db.Document):
    title = StringField()
    content = StringField()
    sender = ReferenceField(User)
    receiver = ReferenceField(User)
    is_read = BooleanField(default=False)
    create_time = DateTimeField(default=datetime.datetime.now)

class WoodsHole(db.Document):
    title = StringField(max_length=20)
    content = StringField(max_length=450)
    like = IntField(default=0)
    comments = ListField(EmbeddedDocumentField(Comment))
    create_time = DateTimeField(default=datetime.datetime.now)

class Sweetie(db.Document):
    content = StringField()
    source = StringField()
    visible = BooleanField()
    create_time = DateTimeField(default=datetime.datetime.now)

class Functions(db.Document):
    tittle = StringField()
    desc = StringField()
    icon = StringField()
    url = StringField()

class SecurityMap(db.Document):
    pass

class CourseData(db.Document):
    #semester = StringField() #16-1 stand for 2016-2017-fall 16-2 for winter semester 
    pass


class MessageBoard(Document):
    content = StringField()
    name = StringField(max_length=20)
    author = ReferenceField(User)
    create_time = DateTimeField(default=datetime.datetime.now)

class LoveBoard(Document):
    content = StringField()
    name = StringField(max_length=20)

class Post(Document):
    title = StringField(max_length=120, required=True)
    content = StringField()
    img = ImageField()
    author = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
