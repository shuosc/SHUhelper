import datetime

from flask import abort
from mongoengine import (BooleanField, DateTimeField, EmailField, ReferenceField, BinaryField, IntField,
                         StringField,ListField)
from UHE.extensions import db
import base64


class Goods(db.Document):
    name = StringField()
    price = IntField()
    record = ListField(DateTimeField(),default=[])
    def to_dict(self):
        return {
            'name': self.name,
            'price': self.price,
            'record': self.record,
            'id': str(self.id)
        }

