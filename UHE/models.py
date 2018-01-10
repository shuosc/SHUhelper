import datetime

from mongoengine import (BooleanField, DateTimeField, Document, StringField)

class Plugin(Document):
    name = StringField()
    status=StringField(default='uninstalled')
    identifier = StringField(unique=True)
    version = StringField()
    author = StringField()
    description = StringField()
    enable = BooleanField(required=True)
    setup_time = DateTimeField(default=datetime.datetime.now)

