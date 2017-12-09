import datetime

from mongoengine import (DateTimeField, ListField, CASCADE,URLField,
                         ReferenceField, StringField, GenericReferenceField)

from UHE.extensions import db

class Link(db.Document):
    identifier = StringField(primary_key=True)
    title = StringField()
    URL = URLField()
    desc = StringField()
    icon = StringField()
    created = DateTimeField(default=datetime.datetime.now)
    meta = {
        'ordering': ['-created'],
        'strict': True
    }