import datetime

from mongoengine import (DateTimeField, ListField,
                         ReferenceField, StringField, GenericReferenceField)

# from config import db
from UHE.extensions import db
from UHE.user.models import User


class Comment(db.Document):
    post = GenericReferenceField()
    display_name = StringField()
    user = ReferenceField(User)
    content = StringField()
    liked = ListField(ReferenceField(User), default=lambda: [])
    created = DateTimeField(datetime.datetime.now)
    meta = {
        'ordering': ['-created'],
        'strict': False
    }
