import datetime

from mongoengine import (DateTimeField, ListField, CASCADE,
                         ReferenceField, StringField, GenericReferenceField)

# from config import db
from UHE.extensions import db

class Publication(db.Document):
    title = StringField()
    content = StringField()
    created = DateTimeField(default=datetime.datetime.now)
    meta = {
        'ordering': ['-created'],
        'strict': True
    }