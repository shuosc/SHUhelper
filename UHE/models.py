import datetime

from mongoengine import (BooleanField, DateTimeField, Document, StringField)


# from config import db

class Plugin(Document):
    name = StringField()
    status=StringField(default='uninstalled')
    identifier = StringField(unique=True)
    version = StringField()
    author = StringField()
    description = StringField()
    enable = BooleanField(required=True)
    setup_time = DateTimeField(default=datetime.datetime.now)


# class Comment(db.Document):
#     post = GenericReferenceField()
#     user = ReferenceField(User)
#     content = StringField()
#     liked = IntField(default=0)
#     created = DateTimeField(datetime.datetime.now)
#     meta = {
#         'ordering': ['-created']
#     }


# class Wiki(Document):
#     title = StringField()
#     content = StringField()
#     tags = ListField(StringField())
#     comments = ListField(EmbeddedDocumentField(Comment))


# class Course(Document):
#     course_no = StringField()
#     course_name = StringField()


# class MessageText(Document):
#     # abstract = StringField()
#     content = StringField()
#     create_time = DateTimeField(default=datetime.datetime.now)

# class Dialog(Document):
#     contact = ReferenceField(User)
#     abstract = StringField()
#     messages_count = IntField()
#     new = BooleanField()
#     create_time = DateTimeField(default=datetime.datetime.now)


