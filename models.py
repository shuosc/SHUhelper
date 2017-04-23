"""
define models
"""
from flask_login import UserMixin
import datetime
from mongoengine import (BooleanField, DateTimeField, Document, EmailField,
                         EmbeddedDocument, EmbeddedDocumentField, ListField,
                         ReferenceField, StringField,ImageField, connect)

connect('psyduck',host='127.0.0.1',port=27017)

class User(UserMixin, Document):
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

class UserData(Document):
    data = StringField()
    site = StringField()
    user = ReferenceField(User)
    last_modified = DateTimeField(default=datetime.datetime.now)

class Messages(Document):
    tittle = StringField()
    content = StringField()
    sender = ReferenceField(User)
    receiver = ReferenceField(User)
    create_time = DateTimeField(default=datetime.datetime.now)

class Sweetie(Document):
    content = StringField()
    source = StringField()
    visible = BooleanField()
    create_time = DateTimeField(default=datetime.datetime.now)

class Functions(Document):
    tittle = StringField()
    desc = StringField()
    icon = StringField()
    url = StringField()

class SecurityMap(Document):
    pass

class CourseData(Document):
    #semester = StringField() #16-1 stand for 2016-2017-fall 16-2 for winter semester 
    pass

class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=450)

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
